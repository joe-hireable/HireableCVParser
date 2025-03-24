import os
import json
import logging
import functions_framework
from typing import Dict, Any, Optional, Tuple, Type
import uuid
from urllib.parse import urlparse

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
    Validate URL format and domain to prevent SSRF attacks.
    
    Args:
        url: URL string to validate
        
    Raises:
        ValueError: If URL format is invalid or domain is not in allowlist
    """
    if not url:
        raise ValueError("URL cannot be empty")
    
    # Allow GCS URLs
    if url.startswith('gs://'):
        return
        
    # Parse URL and validate domain
    try:
        parsed_url = urlparse(url)
        if not parsed_url.scheme in ['http', 'https']:
            raise ValueError(f"Invalid URL scheme: {url}. Only HTTP/HTTPS URLs are allowed")
            
        # Check if the domain is in the allowlist from config
        domain = parsed_url.netloc.lower()
        if not any(domain.endswith(allowed_domain) for allowed_domain in config.ALLOWED_DOMAINS):
            raise ValueError(f"Untrusted domain: {domain}. Only URLs from allowed domains are permitted")
            
    except Exception as e:
        raise ValueError(f"Invalid URL format: {url}. Error: {str(e)}")

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

@functions_framework.http
def cv_optimizer(request):
    with tracer.start_as_current_span("cv_optimizer") as span:
        try:
            # Add request details to span
            span.set_attribute("http.method", request.method)
            span.set_attribute("http.url", request.url)
            request_id = request.headers.get('X-Request-ID', f"req-{uuid.uuid4()}")
            span.set_attribute("request_id", request_id)
            
            # Health check
            if request.method == 'GET' and request.path == '/health':
                return json.dumps({"status": "healthy"}), 200
            
            if request.method != 'POST':
                span.set_attribute("error", True)
                span.set_attribute("error.message", "Only POST method is supported")
                return json.dumps({"error": "Only POST method is supported"}), 405
            
            # Process request with sub-spans
            with tracer.start_span("process_request") as process_span:
                # Initialize clients if needed
                initialize_clients()
                
                try:
                    request_json = request.get_json()
                    cv_url = request_json.get('cv_url')
                    jd_url = request_json.get('jd_url')
                    task = request_json.get('task', 'parsing')
                    section = request_json.get('section')
                    model = request_json.get('model', config.DEFAULT_MODEL)
                    
                    # Validate model selection
                    if model not in config.SUPPORTED_MODELS:
                        raise ValueError(f"Unsupported model: {model}. Must be one of: {', '.join(config.SUPPORTED_MODELS)}")

                    # Add request details to span
                    process_span.set_attribute("task", task)
                    process_span.set_attribute("cv_url", cv_url)
                    process_span.set_attribute("model", model)
                    
                    # Validate task-specific requirements
                    if task in ['parsing', 'scoring']:
                        if not cv_url:
                            raise ValueError(f"CV URL is required for {task} task")
                        if section is not None:
                            raise ValueError(f"Section parameter is not supported for {task} task")
                    
                    # Validate URLs if provided
                    if cv_url:
                        validate_url(cv_url)
                    if jd_url:
                        validate_url(jd_url)
                    
                    # Process documents
                    with tracer.start_span("document_processing") as doc_span:
                        cv_content = doc_processor.download_and_process(cv_url)
                        jd_content = doc_processor.download_and_process(jd_url) if jd_url else ""
                    
                    # Fetch resources with Pydantic model
                    system_prompt, user_prompt_template, few_shot_examples, schema_model = fetch_resources(task)
                    
                    # Format user prompt
                    user_prompt = user_prompt_template.format(
                        section=section,
                        cv_content=cv_content,
                        jd_content=jd_content,
                        few_shot_examples=few_shot_examples
                    )
                    
                    # Generate content using Gemini with Pydantic model and specified model
                    response = gemini_client.generate_content(
                        prompt=user_prompt,
                        response_schema=schema_model,
                        system_prompt=system_prompt,
                        model=model
                    )
                    
                    if response["status"] == "success":
                        return json.dumps(response["data"]), 200
                    else:
                        span.set_attribute("error", True)
                        span.set_attribute("error.message", response["error"])
                        return json.dumps({"error": response["error"]}), 500
                        
                finally:
                    # Clean up resources after processing
                    cleanup_clients()
                    
        except Exception as e:
            span.set_attribute("error", True)
            span.set_attribute("error.message", str(e))
            logger.exception(f"Error in CV optimizer: {e}", extra={'request_id': request_id if 'request_id' in locals() else None})
            return json.dumps({"error": str(e)}), 500 