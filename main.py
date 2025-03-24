import os
import json
import logging
import functions_framework
from typing import Dict, Any, Optional, Tuple
import uuid
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.gcp_trace import GCPTraceExporter

from utils.storage import StorageClient
from utils.document_processor import DocumentProcessor
from utils.gemini_client import GeminiClient
import config

# Initialize OpenTelemetry
tracer_provider = TracerProvider()
tracer_provider.add_span_processor(
    BatchSpanProcessor(GCPTraceExporter())
)
trace.set_tracer_provider(tracer_provider)
tracer = trace.get_tracer(__name__)

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

def validate_url(url: str) -> None:
    """
    Validate URL format.
    
    Args:
        url: URL string to validate
        
    Raises:
        ValueError: If URL format is invalid
    """
    if not url:
        raise ValueError("URL cannot be empty")
    if not (url.startswith('http') or url.startswith('gs://')):
        raise ValueError(f"Invalid URL format: {url}. URL must start with 'http' or 'gs://'")

def load_resource_file(task: str, resource_type: str) -> str:
    """
    Load content from a resource file based on task and type.
    
    Args:
        task: Task name (parsing, ps, cs, ka, role, scoring)
        resource_type: Type of resource (prompt, schema, examples)
        
    Returns:
        Content of the resource file
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    file_paths = {
        'system_prompt': os.path.join(base_dir, 'prompts', 'system_prompt.md'),
        'user_prompt': os.path.join(base_dir, 'prompts', f'{task}_user_prompt.md'),
        'schema': os.path.join(base_dir, 'schemas', f'{task}_schema.json'),
        'examples': os.path.join(base_dir, 'few_shot_examples', f'{task}_few_shot_examples.md')
    }
    
    try:
        with open(file_paths[resource_type], 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        logger.error(f"Error loading resource file {file_paths[resource_type]}: {e}")
        raise

def fetch_resources(task: str) -> Tuple[str, str, str, Dict[str, Any]]:
    """
    Fetch all resources needed for a specific task.
    
    Args:
        task: Task identifier (parsing, ps, cs, etc.)
        
    Returns:
        Tuple of (system prompt, user prompt, few shot examples, schema)
    """
    system_prompt = load_resource_file(task, 'system_prompt')
    user_prompt = load_resource_file(task, 'user_prompt')
    few_shot_examples = load_resource_file(task, 'examples')
    
    schema_text = load_resource_file(task, 'schema')
    schema = json.loads(schema_text)
    
    return system_prompt, user_prompt, few_shot_examples, schema

@functions_framework.http
def cv_optimizer(request):
    """
    Cloud Function to optimize CVs using Gemini API.
    
    Args:
        request: HTTP request object
        
    Returns:
        HTTP response with JSON result
    """
    with tracer.start_as_current_span("cv_optimizer") as span:
        if request.method == 'GET' and request.path == '/health':
            return json.dumps({"status": "healthy"}), 200
        
        if request.method != 'POST':
            return json.dumps({"error": "Only POST method is supported"}), 405
        
        try:
            # Initialize clients if needed
            initialize_clients()
            
            request_json = request.get_json()
            request_id = request.headers.get('X-Request-ID', f"req-{uuid.uuid4()}")
            logger.info(f"Processing request {request_id}", extra={'request_id': request_id})
            
            # Add request_id to span
            span.set_attribute("request_id", request_id)
            
            # Extract parameters
            cv_url = request_json.get('cv_url')
            jd_url = request_json.get('jd_url')
            task = request_json.get('task', 'parsing')  # Default to parsing if not specified
            section = request_json.get('section', '')
            
            # Add task info to span
            span.set_attribute("task", task)
            if section:
                span.set_attribute("section", section)
            
            # Validate task-specific requirements
            if task in ['parsing', 'scoring']:
                if not cv_url:
                    raise ValueError(f"CV URL is required for {task} task")
                if section:
                    raise ValueError(f"Section parameter is not supported for {task} task")
            
            # Validate URLs if provided
            if cv_url:
                validate_url(cv_url)
            if jd_url:
                validate_url(jd_url)
            
            # Process documents with timeout
            try:
                with tracer.start_as_current_span("process_documents"):
                    cv_content = doc_processor.download_and_process(cv_url)
                    jd_content = doc_processor.download_and_process(jd_url) if jd_url else ""
            except TimeoutError:
                span.set_status(trace.Status(trace.StatusCode.ERROR, "Document processing timed out"))
                return json.dumps({"error": "Document processing timed out"}), 504
            
            # Fetch resources
            with tracer.start_as_current_span("fetch_resources"):
                system_prompt, user_prompt_template, few_shot_examples, schema = fetch_resources(task)
            
            # Format user prompt
            user_prompt = user_prompt_template.format(
                section=section,
                cv_content=cv_content,
                jd_content=jd_content,
                few_shot_examples=few_shot_examples
            )
            
            # Generate content using Gemini
            with tracer.start_as_current_span("generate_content"):
                response = gemini_client.generate_content(
                    prompt=user_prompt,
                    schema=schema,
                    system_prompt=system_prompt
                )
            
            if response["status"] == "success":
                span.set_status(trace.Status(trace.StatusCode.OK))
                return json.dumps(response["data"]), 200
            else:
                span.set_status(trace.Status(trace.StatusCode.ERROR, response["error"]))
                return json.dumps({"error": response["error"]}), 500
                
        except Exception as e:
            logger.exception(f"Error in CV optimizer: {e}", extra={'request_id': request_id if 'request_id' in locals() else None})
            span.set_status(trace.Status(trace.StatusCode.ERROR, str(e)))
            return json.dumps({"error": str(e)}), 500 