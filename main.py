"""Main application module for the CV Parser service.

This module implements the core functionality for CV parsing and optimization,
including authentication, request handling, and integration with Google Cloud services.
"""

import os
import json
import logging
import functions_framework
from typing import Dict, Any, Optional, Tuple, Type, Union
import uuid
from urllib.parse import urlparse
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidAudienceError, DecodeError
from flask import Request, make_response, Response, Flask, request, jsonify
import base64
import time
from pydantic import BaseModel, Field, ValidationError
from google.cloud import storage, secretmanager
import google.cloud.logging
import vertexai
from vertexai.language_models import TextGenerationModel
import traceback
from datetime import datetime

from utils.storage import StorageClient
from utils.document_processor import DocumentProcessor
from utils.gemini_client import GeminiClient
from utils.security import (
    rate_limit,
    add_security_headers,
    sanitize_input,
    validate_request_headers,
    validate_json_schema,
    setup_cors
)
import config
from models.schemas import SCHEMA_REGISTRY, BaseResponseSchema

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Google Cloud clients
storage_client: Optional[storage.Client] = None
secret_client: Optional[secretmanager.SecretManagerServiceClient] = None
vertex_client: Optional[TextGenerationModel] = None

def initialize_clients() -> None:
    """Initialize Google Cloud clients with proper error handling.
    
    Sets up connections to Storage, Secret Manager, and Vertex AI services.
    Raises an exception if any client initialization fails.
    """
    global storage_client, secret_client, vertex_client
    
    try:
        storage_client = storage.Client()
        secret_client = secretmanager.SecretManagerServiceClient()
        vertexai.init(project=os.getenv('GOOGLE_CLOUD_PROJECT'))
        vertex_client = TextGenerationModel.from_pretrained("text-bison@001")
        logger.info("Successfully initialized all Google Cloud clients")
    except Exception as e:
        logger.error(f"Failed to initialize clients: {str(e)}")
        raise

def get_secret(secret_id: str) -> str:
    """Retrieve secret from Secret Manager with proper error handling.
    
    Args:
        secret_id: ID of the secret to retrieve
        
    Returns:
        str: Decoded secret value
        
    Raises:
        Exception: If secret retrieval fails
    """
    try:
        name = f"projects/{os.getenv('GOOGLE_CLOUD_PROJECT')}/secrets/{secret_id}/versions/latest"
        response = secret_client.access_secret_version(request={"name": name})
        return response.payload.data.decode("UTF-8")
    except Exception as e:
        logger.error(f"Failed to retrieve secret {secret_id}: {str(e)}")
        raise

def validate_jwt(token: str) -> Dict[str, Any]:
    """Validate JWT token with proper error handling.
    
    Args:
        token: JWT token to validate
        
    Returns:
        Dict[str, Any]: Decoded token payload
        
    Raises:
        jwt.InvalidTokenError: If token is invalid or expired
    """
    try:
        jwt_secret = get_secret('jwt-secret')
        payload = jwt.decode(token, jwt_secret, algorithms=['HS256'])
        
        if 'exp' in payload and datetime.utcnow().timestamp() > payload['exp']:
            raise ExpiredSignatureError("Token has expired")
        
        return payload
    except (ExpiredSignatureError, InvalidAudienceError, DecodeError) as e:
        logger.error(f"JWT validation error: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error during JWT validation: {str(e)}")
        raise

def validate_url(url: str) -> None:
    """Validate URL format and security.
    
    Args:
        url: URL string to validate
        
    Raises:
        ValueError: If URL format is invalid or insecure
    """
    if not url:
        raise ValueError("URL cannot be empty")

    if url.startswith('gs://'):
        return

    if not url.lower().startswith(('http://', 'https://')):
        raise ValueError("URL must start with http:// or https://")

    try:
        parsed_url = urlparse(url)
        if not parsed_url.scheme or not parsed_url.netloc:
            raise ValueError(f"Malformed URL: {url}")
    except Exception as e:
        raise ValueError(f"Invalid URL format: {url}. Error: {str(e)}")

def load_resource_file(task: str, resource_type: str) -> str:
    """Load content from a resource file based on task and type.
    
    Args:
        task: Task identifier (parsing, ps, cs, etc.)
        resource_type: Type of resource (prompt, schema, examples)
        
    Returns:
        str: Content of the resource file
        
    Raises:
        FileNotFoundError: If resource file cannot be found
        ValueError: If resource type is invalid
    """
    if not storage_client:
        initialize_clients()
    
    if config.USE_SECRETS_MANAGER:
        try:
            if resource_type == 'system_prompt':
                return secret_client.get_prompt(task, "system", config.PROMPTS_SECRET_PREFIX)
            elif resource_type == 'user_prompt':
                return secret_client.get_prompt(task, "user", config.PROMPTS_SECRET_PREFIX)
            elif resource_type == 'schema':
                schema_dict = secret_client.get_schema(task, config.SCHEMAS_SECRET_PREFIX)
                return json.dumps(schema_dict) if schema_dict else None
            elif resource_type == 'examples':
                return secret_client.get_examples(task, config.EXAMPLES_SECRET_PREFIX)
            else:
                raise ValueError(f"Invalid resource type: {resource_type}")
        except Exception as e:
            logger.warning(f"Failed to load {resource_type} from Secret Manager: {e}")
    
    # Fall back to GCS
    file_paths = {
        'system_prompt': f'prompts/system_prompt.md',
        'user_prompt': f'prompts/{task}_user_prompt.md',
        'schema': f'schemas/{task}_schema.json',
        'examples': f'few_shot_examples/{task}_few_shot_examples.md'
    }
    
    try:
        content = storage_client.read_file(file_paths[resource_type])
        if content is None:
            raise FileNotFoundError(f"Could not read file from GCS: {file_paths[resource_type]}")
        return content
    except Exception as e:
        logger.error(f"Error loading resource file {file_paths[resource_type]}: {e}")
        raise

def fetch_resources(task: str) -> Tuple[str, str, str, Type[BaseResponseSchema]]:
    """Fetch all resources needed for a specific task.
    
    Args:
        task: Task identifier (parsing, ps, cs, etc.)
        
    Returns:
        Tuple[str, str, str, Type[BaseResponseSchema]]: System prompt, user prompt,
            few shot examples, and schema model class
        
    Raises:
        ValueError: If required resources cannot be loaded or schema model is not found
    """
    try:
        system_prompt = load_resource_file(task, 'system_prompt')
        user_prompt = load_resource_file(task, 'user_prompt')
        few_shot_examples = load_resource_file(task, 'examples')
        
        schema_model = SCHEMA_REGISTRY.get(task)
        if not schema_model:
            raise ValueError(f"No schema model found for task: {task}")

        # Validate schema consistency
        try:
            schema_json = load_resource_file(task, 'schema')
            if schema_json:
                schema_dict = json.loads(schema_json)
                pydantic_schema = schema_model.model_json_schema()
                
                # Validate schema structure
                required_fields = ['properties', 'required', 'type', '$defs']
                missing_fields = [f for f in required_fields if f not in schema_dict and f in pydantic_schema]
                if missing_fields:
                    logger.warning(f"Schema file for task '{task}' is missing fields: {', '.join(missing_fields)}")
                
                # Validate property consistency
                if 'properties' in schema_dict and 'properties' in pydantic_schema:
                    file_props = set(schema_dict['properties'].keys())
                    model_props = set(pydantic_schema['properties'].keys())
                    missing_in_file = model_props - file_props
                    if missing_in_file:
                        logger.warning(f"Schema file for task '{task}' is missing properties: {', '.join(missing_in_file)}")
        except Exception as e:
            logger.warning(f"Error validating schema for task '{task}': {str(e)}")
        
        return system_prompt, user_prompt, few_shot_examples, schema_model
        
    except Exception as e:
        logger.error(f"Error fetching resources for task '{task}': {str(e)}")
        raise ValueError(f"Failed to fetch resources for task '{task}': {str(e)}")

@functions_framework.http
@rate_limit()
def cv_optimizer(request: Request) -> Response:
    """Main Cloud Function handler for CV optimization.
    
    Handles CORS, authentication, and processes CV/JD data. Expects
    multipart/form-data with 'cv_file' and form fields like 'task', 'jd'.
    
    Args:
        request: Flask Request object
        
    Returns:
        Response: Processed response with appropriate headers
    """
    # Handle CORS preflight
    if request.method == 'OPTIONS':
        return setup_cors(request)

    # Initialize request context
    request_id = request.headers.get('X-Request-ID', str(uuid.uuid4()))
    logger.info(f"Processing request {request_id}", extra={'request_id': request_id})
    
    try:
        # Validate request headers
        header_error = validate_request_headers(request)
        if header_error:
            return add_security_headers(header_error)
        
        # Authenticate request
        auth_error = authenticate_request(request)
        if auth_error:
            return add_security_headers(auth_error)
        
        # Process request based on method
        if request.method == 'GET':
            if request.path == '/health':
                return add_security_headers(make_response(jsonify({"status": "healthy"}), 200))
            return add_security_headers(make_response(jsonify({"error": "Method not allowed"}), 405))
        
        # Handle POST request
        if request.method == 'POST':
            return process_post_request(request, request_id)
            
        return add_security_headers(make_response(jsonify({"error": "Method not allowed"}), 405))
        
    except Exception as e:
        logger.error(f"Error processing request {request_id}: {str(e)}", exc_info=True)
        return add_security_headers(make_response(
            jsonify({"error": "Internal server error", "request_id": request_id}),
            500
        ))

def authenticate_request(request: Request) -> Optional[Response]:
    """Authenticate the incoming request.
    
    Supports both GCP IAM and Supabase JWT authentication.
    
    Args:
        request: Flask Request object
        
    Returns:
        Optional[Response]: Error response if authentication fails, None if successful
    """
    gcp_auth_user = request.headers.get('X-Goog-Authenticated-User-Email')
    gcp_iap_user = request.headers.get('X-Goog-IAP-JWT-Assertion')
    
    if gcp_auth_user or gcp_iap_user:
        auth_user = gcp_auth_user or "IAP Authenticated User"
        logger.info(f"GCP authenticated user: {auth_user}")
        return None
    
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return make_response(jsonify({"error": "No authorization header"}), 401)
    
    try:
        jwt_payload = validate_jwt(auth_header.split(' ')[1])
        if not jwt_payload.get('sub'):
            raise ValueError("User ID ('sub') not found in JWT payload")
        logger.info(f"Authenticated user: {jwt_payload['sub']}")
        return None
    except Exception as e:
        logger.warning(f"Authentication failed: {str(e)}")
        return make_response(jsonify({"error": f"Unauthorized: {str(e)}"}), 401)

def process_post_request(request: Request, request_id: str) -> Response:
    """Process POST request for CV optimization.
    
    Args:
        request: Flask Request object
        request_id: Unique request identifier
        
    Returns:
        Response: Processed response with results
    """
    try:
        # Validate request data
        if not request.files.get('cv_file'):
            return make_response(jsonify({"error": "No CV file provided"}), 400)
            
        task = request.form.get('task')
        if not task or task not in SCHEMA_REGISTRY:
            return make_response(jsonify({"error": "Invalid task specified"}), 400)
            
        # Load required resources
        system_prompt, user_prompt, few_shot_examples, schema_model = fetch_resources(task)
        
        # Process CV file - handle as binary
        cv_file = request.files['cv_file']
        cv_content = cv_file.read()  # Keep as bytes
        
        # Get optional JD if provided
        jd_content = None
        if 'jd_file' in request.files:
            jd_file = request.files['jd_file']
            jd_content = jd_file.read()  # Keep as bytes
        
        # Initialize clients if needed
        if not storage_client:
            initialize_clients()
        
        # Process document
        processor = DocumentProcessor(
            storage_client=storage_client,
            vertex_client=vertex_client,
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            few_shot_examples=few_shot_examples,
            schema_model=schema_model
        )
        
        result = processor.process_document(cv_content, jd_content)
        
        return add_security_headers(make_response(
            jsonify({"result": result, "request_id": request_id}),
            200
        ))
        
    except Exception as e:
        logger.error(f"Error processing POST request {request_id}: {str(e)}", exc_info=True)
        error_message = str(e)
        if "Vertex AI error" in error_message:
            return make_response(
                jsonify({"error": error_message, "request_id": request_id}),
                500
            )
        return make_response(
            jsonify({"error": "Failed to process request", "request_id": request_id}),
            500
        ) 