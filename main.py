import os
import json
import logging
import functions_framework
from typing import Dict, Any, Optional, Tuple, Type
import uuid
from urllib.parse import urlparse
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidAudienceError, DecodeError
from flask import Request, make_response, Response

from utils.storage import StorageClient
from utils.document_processor import DocumentProcessor
from utils.gemini_client import GeminiClient
import config
from opentelemetry import trace
from opentelemetry.exporter.cloud_trace import CloudTraceSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.propagate import set_global_textmap
from opentelemetry.propagators.cloud_trace_propagator import CloudTraceFormatPropagator
from models.schemas import SCHEMA_REGISTRY, BaseResponseSchema

class StructuredLogFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name
        }
        if hasattr(record, 'request_id'):
            log_record["request_id"] = record.request_id
        return json.dumps(log_record)

# Configure logging
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setFormatter(StructuredLogFormatter())
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# Initialize tracing (add this after your logging setup)
tracer_provider = TracerProvider()
cloud_trace_exporter = CloudTraceSpanExporter()
tracer_provider.add_span_processor(BatchSpanProcessor(cloud_trace_exporter))
trace.set_tracer_provider(tracer_provider)
set_global_textmap(CloudTraceFormatPropagator())

# Get a tracer
tracer = trace.get_tracer(__name__)

# Global client instances for pooling
storage_client = None
gemini_client = None
doc_processor = None

def initialize_clients():
    """Initialize global client instances if they haven't been created yet."""
    global storage_client, gemini_client, doc_processor
    
    if not storage_client:
        storage_client = StorageClient(config.GCS_BUCKET_NAME)
    if not gemini_client:
        gemini_client = GeminiClient(
            project_id=config.PROJECT_ID,
            location=config.LOCATION
        )
    if not doc_processor:
        doc_processor = DocumentProcessor()

def cleanup_clients():
    """Clean up global client instances."""
    global storage_client, gemini_client, doc_processor
    
    if doc_processor:
        doc_processor.cleanup()
        doc_processor = None
    if storage_client:
        storage_client = None
    if gemini_client:
        gemini_client = None

def validate_url(url: str) -> None:
    """
    Validate URL format to ensure it starts with http or https.

    Args:
        url: URL string to validate

    Raises:
        ValueError: If URL format is invalid
    """
    if not url:
        raise ValueError("URL cannot be empty")

    # Allow GCS URLs (or remove if not needed)
    if url.startswith('gs://'):
        return # Keep if GCS interaction is still required

    # Basic check for http/https schemes
    if not url.lower().startswith(('http://', 'https://')):
         raise ValueError(f"Invalid URL: {url}. Only HTTP/HTTPS URLs are allowed")

    # Optional: Minimal parsing to catch very malformed URLs, but avoid strict validation
    # try:
    #     parsed_url = urlparse(url)
    #     if not parsed_url.scheme or not parsed_url.netloc:
    #         raise ValueError(f"Malformed URL: {url}")
    # except Exception as e:
    #     raise ValueError(f"Invalid URL format: {url}. Error: {str(e)}")

def load_resource_file(task: str, resource_type: str) -> str:
    """
    Load content from a resource file based on task and type.
    
    Args:
        task: Task name (parsing, ps, cs, ka, role, scoring)
        resource_type: Type of resource (prompt, schema, examples)
        
    Returns:
        Content of the resource file
    """
    # Define GCS paths instead of local paths
    file_paths = {
        'system_prompt': 'prompts/system_prompt.md',
        'user_prompt': f'prompts/{task}_user_prompt.md',
        'schema': f'schemas/{task}_schema.json',
        'examples': f'few_shot_examples/{task}_few_shot_examples.md'
    }
    
    try:
        # Use the global storage client that's properly initialized
        global storage_client
        if not storage_client:
            initialize_clients()
            
        content = storage_client.read_file(file_paths[resource_type])
        if content is None:
            raise FileNotFoundError(f"Could not read file from GCS: {file_paths[resource_type]}")
        return content
    except Exception as e:
        logger.error(f"Error loading resource file {file_paths[resource_type]}: {e}")
        raise

def fetch_resources(task: str) -> Tuple[str, str, str, Type[BaseResponseSchema]]:
    """
    Fetch all resources needed for a specific task.
    
    Args:
        task: Task identifier (parsing, ps, cs, etc.)
        
    Returns:
        Tuple of (system prompt, user prompt, few shot examples, schema model class)
    """
    system_prompt = load_resource_file(task, 'system_prompt')
    user_prompt = load_resource_file(task, 'user_prompt')
    few_shot_examples = load_resource_file(task, 'examples')
    
    # Get the appropriate Pydantic model class for the task
    schema_model = SCHEMA_REGISTRY.get(task)
    if not schema_model:
        raise ValueError(f"No schema model found for task: {task}")
    
    return system_prompt, user_prompt, few_shot_examples, schema_model

# --- CORS Helper Functions ---
# REMOVED: ALLOWED_ORIGINS = os.environ.get("ALLOWED_ORIGINS", "http://localhost:5173").split(',')

def _build_cors_preflight_response():
    """Builds a CORS preflight response allowing any origin."""
    response = make_response()
    # Allow any origin
    response.headers.add("Access-Control-Allow-Origin", "*")
    # Specify allowed headers and methods
    response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization,X-Request-ID") # Add any other headers your frontend sends
    response.headers.add("Access-Control-Allow-Methods", "POST, GET, OPTIONS") # Add GET if used
    response.status_code = 204 # No Content for preflight
    return response

def _corsify_actual_response(response: Response):
    """Adds permissive CORS headers to an actual response."""
    # Allow any origin
    response.headers.add("Access-Control-Allow-Origin", "*")
    # Optional: Explicitly expose headers if needed by the frontend
    # response.headers.add("Access-Control-Expose-Headers", "Content-Disposition")
    return response

# --- Supabase JWT Verification ---
SUPABASE_JWT_SECRET = os.environ.get("SUPABASE_JWT_SECRET")
SUPABASE_PROJECT_REF = os.environ.get("SUPABASE_PROJECT_REF")

def verify_supabase_jwt(auth_header: Optional[str]) -> Dict[str, Any]:
    """
    Verifies the Supabase JWT from the Authorization header.

    Args:
        auth_header: The content of the Authorization header (e.g., "Bearer <token>").

    Returns:
        The decoded JWT payload if valid.

    Raises:
        ValueError: If the header is missing, malformed, or the token is invalid/expired.
    """
    if not SUPABASE_JWT_SECRET or not SUPABASE_PROJECT_REF:
        logger.error("SUPABASE_JWT_SECRET or SUPABASE_PROJECT_REF environment variable not set.")
        raise ValueError("Authentication configuration error.")

    if not auth_header:
        raise ValueError("Authorization header is missing.")

    parts = auth_header.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise ValueError("Invalid Authorization header format. Expected 'Bearer <token>'.")

    token = parts[1]
    expected_issuer = f"https://{SUPABASE_PROJECT_REF}.supabase.co/auth/v1"
    expected_audience = "authenticated"

    try:
        payload = jwt.decode(
            token,
            SUPABASE_JWT_SECRET,
            algorithms=["HS256"],
            audience=expected_audience,
            issuer=expected_issuer
        )
        # Check 'sub' claim exists
        if 'sub' not in payload:
            raise ValueError("Token is missing 'sub' (subject) claim.")
        return payload
    except ExpiredSignatureError:
        raise ValueError("Token has expired.")
    except InvalidAudienceError:
        raise ValueError(f"Invalid token audience. Expected '{expected_audience}'.")
    except jwt.InvalidIssuerError:
         raise ValueError(f"Invalid token issuer. Expected '{expected_issuer}'.")
    except DecodeError as e:
        raise ValueError(f"Token decode error: {e}")
    except Exception as e:
        raise ValueError(f"An unexpected error occurred during token verification: {e}")

@functions_framework.http
def cv_optimizer(request: Request):
    """
    Main Cloud Function handler. Handles CORS, JWT auth, and processes CV/JD.
    Expects multipart/form-data with 'cv_file' and form fields like 'task', 'jd'.
    """
    # --- CORS Preflight Handling ---
    if request.method == 'OPTIONS':
        return _build_cors_preflight_response()

    # --- Actual Request Handling ---
    with tracer.start_as_current_span("cv_optimizer") as span:
        request_id = request.headers.get('X-Request-ID', f"req-{uuid.uuid4()}")
        span.set_attribute("request_id", request_id)
        span.set_attribute("http.method", request.method)
        span.set_attribute("http.url", request.url)
        span.set_attribute("content_type", request.content_type) # Log content type

        user_id = None # Initialize user_id

        try:
            # --- Authentication ---
            with tracer.start_span("authenticate_request") as auth_span:
                auth_header = request.headers.get("Authorization")
                try:
                    # Verify JWT and extract user ID ('sub' claim)
                    jwt_payload = verify_supabase_jwt(auth_header)
                    user_id = jwt_payload.get('sub')
                    if not user_id:
                         raise ValueError("User ID ('sub') not found in JWT payload.")
                    auth_span.set_attribute("user.id", user_id)
                    logger.info(f"Authenticated user: {user_id}", extra={'request_id': request_id})
                except ValueError as auth_error:
                    auth_span.set_attribute("error", True)
                    auth_span.set_attribute("error.message", str(auth_error))
                    logger.warning(f"Authentication failed: {auth_error}", extra={'request_id': request_id})
                    response = make_response(json.dumps({"error": f"Unauthorized: {auth_error}"}), 401)
                    return _corsify_actual_response(response)

            # Health check (moved after auth for consistency, or keep public if needed)
            if request.method == 'GET' and request.path == '/health':
                 response = make_response(json.dumps({"status": "healthy"}), 200)
                 return _corsify_actual_response(response)

            if request.method != 'POST':
                span.set_attribute("error", True)
                span.set_attribute("error.message", "Only POST method is supported")
                response = make_response(json.dumps({"error": "Only POST method is supported"}), 405)
                return _corsify_actual_response(response)

            # --- Process Request ---
            with tracer.start_span("process_request") as process_span:
                initialize_clients() # Initialize clients per request

                try:
                    # Extract data from multipart/form-data
                    if not request.content_type or not request.content_type.startswith('multipart/form-data'):
                         raise ValueError("Invalid Content-Type. Expected 'multipart/form-data'.")

                    # --- Get CV File ---
                    if 'cv_file' not in request.files:
                        raise ValueError("Missing 'cv_file' in request files.")
                    cv_file = request.files['cv_file']
                    cv_filename = cv_file.filename or "untitled_cv"
                    cv_content_type = cv_file.content_type or 'application/octet-stream'
                    cv_bytes = cv_file.read()
                    if not cv_bytes:
                         raise ValueError("'cv_file' cannot be empty.")

                    # --- Get Form Parameters ---
                    task = request.form.get('task', 'parsing')
                    jd_input = request.form.get('jd') # Raw input: URL, GCS path, or text
                    section = request.form.get('section')
                    model = request.form.get('model', config.DEFAULT_MODEL)

                    # Validate model selection
                    if model not in config.SUPPORTED_MODELS:
                        raise ValueError(f"Unsupported model: {model}. Must be one of: {', '.join(config.SUPPORTED_MODELS)}")

                    process_span.set_attribute("task", task)
                    process_span.set_attribute("model", model)
                    process_span.set_attribute("cv_filename", cv_filename)
                    process_span.set_attribute("cv_content_type", cv_content_type)
                    process_span.set_attribute("user_id", user_id) # Add user ID to span

                    # Validate task-specific requirements
                    if task in ['parsing', 'scoring']:
                        # CV is now handled via file upload
                        if section is not None:
                            raise ValueError(f"Section parameter is not supported for {task} task")
                    # Add other task-specific validations if needed

                    # --- Upload CV to GCS ---
                    with tracer.start_span("upload_cv_to_gcs") as upload_span:
                        gcs_cv_filename = f"{uuid.uuid4()}_{cv_filename}"
                        gcs_cv_path = f"uploads/{user_id}/{gcs_cv_filename}" # User-specific path
                        cv_gcs_uri = storage_client.save_bytes_to_gcs(cv_bytes, gcs_cv_path, cv_content_type)
                        if not cv_gcs_uri:
                             raise IOError("Failed to upload CV file to GCS.")
                        upload_span.set_attribute("gcs_uri", cv_gcs_uri)
                        logger.info(f"CV uploaded for user {user_id} to {cv_gcs_uri}", extra={'request_id': request_id})

                    # --- Process CV ---
                    with tracer.start_span("process_cv") as cv_proc_span:
                         cv_proc_span.set_attribute("cv_gcs_uri", cv_gcs_uri)
                         cv_content = doc_processor.download_and_process(cv_gcs_uri)
                         if cv_content is None:
                             raise ValueError(f"Failed to process CV from GCS URI: {cv_gcs_uri}")
                         cv_proc_span.set_attribute("cv_content.length", len(cv_content))


                    # --- Process JD ---
                    jd_content = ""
                    jd_gcs_uri = None # URI if JD is a file processed from URL/GCS
                    with tracer.start_span("process_jd") as jd_proc_span:
                        if jd_input:
                            jd_proc_span.set_attribute("jd_input_type", "url/gcs/text")
                            if jd_input.startswith(('http://', 'https://', 'gs://')):
                                # Handle URL/GCS path for JD
                                validate_url(jd_input) # Reuse existing validation
                                jd_proc_span.set_attribute("jd_source_uri", jd_input)

                                if jd_input.startswith('gs://'):
                                    jd_gcs_uri = jd_input
                                    jd_content = doc_processor.download_and_process(jd_gcs_uri)
                                else: # HTTP(S) URL
                                    if jd_input.lower().endswith('.pdf'):
                                        # Direct PDF URL
                                        jd_gcs_uri = storage_client.save_url_to_gcs(jd_input, f"uploads/{user_id}/jds/{uuid.uuid4()}.pdf")
                                    else:
                                        # Webpage URL -> convert to PDF in GCS
                                        pdf_path = f"uploads/{user_id}/jds/{uuid.uuid4()}.pdf"
                                        jd_gcs_uri = storage_client.save_webpage_as_pdf(jd_input, pdf_path)

                                    if not jd_gcs_uri:
                                         raise IOError(f"Failed to save JD from URL {jd_input} to GCS.")
                                    jd_content = doc_processor.download_and_process(jd_gcs_uri)

                                if jd_content is None:
                                    raise ValueError(f"Failed to process JD from source: {jd_input}")

                            else:
                                # Handle raw text JD input
                                jd_proc_span.set_attribute("jd_input_type", "text")
                                jd_content = jd_input # Assume it's raw text

                            jd_proc_span.set_attribute("jd_content.length", len(jd_content))
                            if jd_gcs_uri:
                                jd_proc_span.set_attribute("jd_gcs_uri", jd_gcs_uri)


                    # --- Fetch LLM Resources ---
                    system_prompt, user_prompt_template, few_shot_examples, schema_model = fetch_resources(task)

                    # Format user prompt
                    user_prompt = user_prompt_template.format(
                        section=section if section else "N/A", # Handle potential None
                        cv_content=cv_content,
                        jd_content=jd_content if jd_content else "N/A", # Handle empty JD
                        few_shot_examples=few_shot_examples
                    )

                    # --- Generate Content using Gemini ---
                    with tracer.start_span("generate_gemini_content") as gemini_span:
                        gemini_span.set_attribute("model", model)
                        # Pass JD GCS URI if it exists and model supports multimodal
                        # Check if model is multimodal before passing file_uri
                        # For now, assume multimodal models might benefit from JD file
                        file_uri_to_pass = jd_gcs_uri if jd_gcs_uri else None
                        mime_type_to_pass = "application/pdf" if file_uri_to_pass else None

                        response_data = gemini_client.generate_content(
                            prompt=user_prompt,
                            response_schema=schema_model,
                            system_prompt=system_prompt,
                            model=model,
                            file_uri=file_uri_to_pass, # Pass JD URI if available
                            mime_type=mime_type_to_pass
                        )

                        gemini_span.set_attribute("response.status", response_data["status"])
                        if response_data["status"] == "error":
                            gemini_span.set_attribute("error", True)
                            gemini_span.set_attribute("error.message", response_data["error"])

                    # --- Handle Response ---
                    if response_data["status"] == "success":
                        response = make_response(json.dumps(response_data["data"]), 200)
                        response.headers['Content-Type'] = 'application/json'
                        return _corsify_actual_response(response)
                    else:
                        # Log error from Gemini client
                        error_msg = response_data.get("error", "Unknown error during content generation")
                        logger.error(f"Gemini content generation failed: {error_msg}", extra={'request_id': request_id})
                        span.set_attribute("error", True)
                        span.set_attribute("error.message", f"Content generation failed: {error_msg}")
                        response = make_response(json.dumps({"error": f"Content generation failed: {error_msg}"}), 500)
                        return _corsify_actual_response(response)

                finally:
                    # Clean up clients after processing each request
                    cleanup_clients()

        except ValueError as ve: # Specific user input errors (4xx)
            span.set_attribute("error", True)
            span.set_attribute("error.message", str(ve))
            logger.warning(f"Validation Error: {ve}", extra={'request_id': request_id})
            response = make_response(json.dumps({"error": str(ve)}), 400) # Bad Request
            return _corsify_actual_response(response)
        except IOError as ioe: # File handling errors (5xx)
            span.set_attribute("error", True)
            span.set_attribute("error.message", str(ioe))
            logger.error(f"IO Error: {ioe}", extra={'request_id': request_id})
            response = make_response(json.dumps({"error": f"Internal Server Error: {ioe}"}), 500)
            return _corsify_actual_response(response)
        except Exception as e: # General errors (5xx)
            span.set_attribute("error", True)
            span.set_attribute("error.message", str(e))
            logger.exception(f"Unhandled Error in CV optimizer: {e}", extra={'request_id': request_id})
            response = make_response(json.dumps({"error": "An unexpected internal error occurred."}), 500)
            return _corsify_actual_response(response) 