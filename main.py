"""
CV Optimizer Cloud Function
--------------------------
This function orchestrates API calls to Gemini 2.0 Flash Lite for CV optimization tasks.
"""

import os
import json
import logging
import functions_framework
from typing import Dict, Any, Optional, Tuple

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
    Fetch all necessary resources for a given task.
    
    Args:
        task: Task name
        
    Returns:
        Tuple of (system_prompt, user_prompt, few_shot_examples, schema)
    """
    system_prompt = load_resource_file(task, 'system_prompt')
    user_prompt = load_resource_file(task, 'user_prompt')
    few_shot_examples = load_resource_file(task, 'examples')
    
    # Load and parse schema
    schema_content = load_resource_file(task, 'schema')
    schema = json.loads(schema_content)
    
    return system_prompt, user_prompt, few_shot_examples, schema

@functions_framework.http
def cv_optimizer(request):
    """
    Cloud Function entry point for CV optimization tasks.
    """
    # Set CORS headers for preflight request
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }
        return ('', 204, headers)

    # Set CORS headers for main request
    headers = {'Access-Control-Allow-Origin': '*'}
    
    try:
        # Parse request data
        request_json = request.get_json(silent=True)
        if not request_json:
            return (json.dumps({"error": "No JSON data provided"}), 400, headers)
        
        # Extract parameters
        cv_url = request_json.get('cv_url')
        jd_url = request_json.get('jd_url')
        task = request_json.get('task')
        section = request_json.get('section')
        
        # Validate task parameter
        if not task:
            return (json.dumps({"error": "Missing required 'task' parameter"}), 400, headers)
        
        if task not in config.ALLOWED_TASKS:
            return (json.dumps(
                {"error": f"Invalid task. Allowed values: {', '.join(config.ALLOWED_TASKS)}"}
            ), 400, headers)
        
        # Initialize clients
        storage_client = StorageClient(config.GCS_BUCKET_NAME)
        doc_processor = DocumentProcessor()
        gemini_client = GeminiClient(config.PROJECT_ID, config.LOCATION)
        
        # Process documents
        cv_content = None
        jd_content = None
        
        if cv_url:
            try:
                cv_content = doc_processor.download_and_process(cv_url)
                if cv_content:
                    storage_client.upload_file(cv_content, config.CV_FOLDER)
            except Exception as e:
                logger.error(f"Error processing CV: {e}")
        
        if jd_url:
            try:
                jd_content = doc_processor.download_and_process(jd_url)
                if jd_content:
                    storage_client.upload_file(jd_content, config.JD_FOLDER)
            except Exception as e:
                logger.error(f"Error processing JD: {e}")
        
        # Fetch resources
        system_prompt, user_prompt, few_shot_examples, schema = fetch_resources(task)
        
        # Prepare prompt with variables
        user_prompt_with_vars = user_prompt.format(
            section=section or "",
            cv_content=cv_content or "",
            jd_content=jd_content or "",
            few_shot_examples=few_shot_examples
        )
        
        # Call Gemini model
        response = gemini_client.generate_text(
            prompt=user_prompt_with_vars,
            schema=schema,
            system_instruction=system_prompt
        )
        
        # Process response
        if isinstance(response, dict) and response.get("status") == "success":
            # Strip status and errors, return only data
            result = response.get("data", {})
            return (json.dumps(result), 200, headers)
        else:
            # Return the full response
            return (json.dumps(response), 200, headers)
        
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        return (json.dumps({"error": str(e)}), 500, headers) 