import os
import json
import logging
import functions_framework
from typing import Dict, Any, Optional, Tuple
import uuid

from utils.storage import StorageClient
from utils.document_processor import DocumentProcessor
from utils.gemini_client import GeminiClient
import config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    if request.method == 'GET' and request.path == '/health':
        return json.dumps({"status": "healthy"}), 200
    
    if request.method != 'POST':
        return json.dumps({"error": "Only POST method is supported"}), 405
    
    try:
        request_json = request.get_json()
        request_id = request.headers.get('X-Request-ID', f"req-{uuid.uuid4()}")
        logger.info(f"Processing request {request_id}")
        
        # Extract parameters
        cv_url = request_json.get('cv_url')
        jd_url = request_json.get('jd_url')
        task = request_json.get('task', 'parsing')  # Default to parsing if not specified
        section = request_json.get('section', '')
        
        # Initialize clients
        doc_processor = DocumentProcessor()
        storage_client = StorageClient(config.GCS_BUCKET_NAME)
        gemini_client = GeminiClient(
            project_id=config.PROJECT_ID,
            location=config.LOCATION,
            key_path=config.SERVICE_ACCOUNT_KEY_PATH
        )
        
        # Process documents with timeout
        try:
            cv_content = doc_processor.download_and_process(cv_url)
            jd_content = doc_processor.download_and_process(jd_url) if jd_url else ""
        except TimeoutError:
            return json.dumps({"error": "Document processing timed out"}), 504
        
        # Fetch resources
        system_prompt, user_prompt_template, few_shot_examples, schema = fetch_resources(task)
        
        # Format user prompt
        user_prompt = user_prompt_template.format(
            section=section,
            cv_content=cv_content,
            jd_content=jd_content,
            few_shot_examples=few_shot_examples
        )
        
        # Generate content using Gemini
        response = gemini_client.generate_content(
            prompt=user_prompt,
            schema=schema,
            system_prompt=system_prompt
        )
        
        if response["status"] == "success":
            return json.dumps(response["data"]), 200
        else:
            return json.dumps({"error": response["error"]}), 500
            
    except Exception as e:
        logger.exception(f"Error in CV optimizer: {e}")
        return json.dumps({"error": str(e)}), 500 