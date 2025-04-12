import os
import json
import logging
import time
import re
from typing import Dict, Any, Optional, List, Type, Union
from google import genai
from google.genai.types import HttpOptions, Part, GenerateContentConfig
from google.cloud import aiplatform
from config import VERTEX_AI_ENABLED
from opentelemetry import trace
import base64
from pydantic import BaseModel, ValidationError
from models.schemas import BaseResponseSchema, SCHEMA_REGISTRY

logger = logging.getLogger(__name__)

class GeminiClient:
    """Client for interacting with Gemini API via Google Generative AI or Vertex AI."""
    
    def __init__(self, project_id: str, location: str = "us-central1"):
        """
        Initialize the Gemini client.
        
        Args:
            project_id: Google Cloud project ID
            location: Google Cloud region (default: europe-west2 for London)
            
        Raises:
            Exception: If client initialization fails
        """
        self.project_id = project_id
        self.location = location
        
        # Retry configuration
        self.max_retries = 3
        self.base_delay = 1  # Base delay in seconds
        self.max_delay = 10  # Maximum delay in seconds
        
        self.tracer = trace.get_tracer(__name__)
        
        # Default generation config
        self.default_config = {
            "temperature": 0.5,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 8192,
            "candidate_count": 1
        }
        
        # Model name for Gemini 2.0 Flash
        self.model_name = "gemini-2.0-flash-001"
        
        # Initialize the appropriate client based on configuration
        self.use_vertex_ai = VERTEX_AI_ENABLED
        
        try:
            if self.use_vertex_ai:
                # Initialize Vertex AI
                aiplatform.init(project=project_id, location=location)
                self.client = genai.Client(
                    vertexai=True,
                    project=project_id,
                    location=location
                )
                logger.info(f"Initialized Vertex AI client for project {project_id} in {location}")
            else:
                # Initialize Google Generative AI with API key
                api_key = os.environ.get("GOOGLE_API_KEY")
                if not api_key:
                    raise ValueError("GOOGLE_API_KEY environment variable is required for non-Vertex AI usage")
                
                self.client = genai.Client(api_key=api_key)
                logger.info(f"Initialized Google Generative AI client with API key")
                
        except Exception as e:
            logger.error(f"Failed to initialize Gemini client: {str(e)}")
            raise
    
    def _calculate_retry_delay(self, attempt: int) -> float:
        """Calculate exponential backoff delay with jitter."""
        with self.tracer.start_as_current_span("calculate_retry_delay") as span:
            span.set_attribute("attempt", attempt)
            delay = min(self.base_delay * (2 ** attempt), self.max_delay)  # Exponential backoff
            jitter = delay * 0.1 * (time.time() % 1)  # Add 10% jitter
            final_delay = delay + jitter
            span.set_attribute("delay", final_delay)
            return final_delay
    
    def generate_content(
        self,
        prompt: str,
        response_schema: Optional[Union[Type[BaseResponseSchema], Dict[str, Any]]] = None,
        system_prompt: Optional[str] = None,
        config: Optional[Dict[str, Any]] = None,
        file_uri: Optional[str] = None,
        mime_type: str = "application/pdf",
        model: Optional[str] = None
    ) -> Dict[str, Any]:
        with self.tracer.start_as_current_span("generate_content") as span:
            span.set_attribute("prompt.length", len(prompt))
            span.set_attribute("has_system_prompt", system_prompt is not None)
            span.set_attribute("model", model or self.model_name)
            
            attempt = 0
            last_error = None
            
            while attempt <= self.max_retries:
                try:
                    
                    # Format system instruction correctly
                    system_instruction = Part.from_text(text=system_prompt) if system_prompt else None
                    
                    # Prepare generation config
                    config_params = self.default_config.copy()
                    if config:
                        config_params.update(config)
                    
                    # Convert Pydantic model to dictionary schema if needed
                    schema_dict = None
                    if response_schema:
                        if isinstance(response_schema, type) and issubclass(response_schema, BaseResponseSchema):
                            schema_dict = response_schema.model_json_schema()
                        else:
                            schema_dict = response_schema

                    # Create proper GenerateContentConfig
                    generation_config = GenerateContentConfig(
                        temperature=config_params.get("temperature", 0.5),
                        top_p=config_params.get("top_p", 0.95),
                        top_k=config_params.get("top_k", 40),
                        max_output_tokens=config_params.get("max_output_tokens", 8192),
                        candidate_count=config_params.get("candidate_count", 1),
                        system_instruction=system_instruction,
                        response_mime_type="application/json" if schema_dict else None,
                        response_schema=schema_dict
                    )
                    
                    # Prepare properly typed content
                    content_parts = []
                    if file_uri:
                        # Add file part if provided
                        content_parts.append(Part.from_uri(uri=file_uri, mime_type=mime_type))
                    
                    # Add text prompt
                    if prompt:
                        content_parts.append(Part.from_text(text=prompt))
                    
                    # Create content with role
                    contents = [genai.types.Content(role="user", parts=content_parts)]
                    
                    # Use provided model or fall back to default
                    model_name = model or self.model_name

                    # Generate content using the client with specified model name
                    model_client = self.client.models.get(model_name)
                    
                    # Apply safety settings if needed
                    # safety_settings = {
                    #    genai.types.HarmCategory.HARM_CATEGORY_HARASSMENT: 
                    #        genai.types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
                    # }
                    
                    response = model_client.generate_content(
                        contents=contents,
                        generation_config=generation_config,
                        # safety_settings=safety_settings
                    )
                    
                    # Handle schema-based responses
                    if response_schema:
                        try:
                            # Clean and parse JSON response
                            text = response.text
                            # Log the raw response for debugging
                            logger.debug(f"Raw response text: {text[:1000]}...")
                            
                            # Clean up JSON from markdown formatting
                            if text.startswith("```json"):
                                text = text[7:]
                            elif text.startswith("```"):
                                text = text[3:]
                            if text.endswith("```"):
                                text = text[:-3]
                            
                            # Try to parse JSON
                            parsed_json = None
                            json_errors = []
                            
                            # First attempt: direct parsing
                            try:
                                parsed_json = json.loads(text.strip())
                            except json.JSONDecodeError as e:
                                json_errors.append(f"Initial JSON parsing error: {e}")
                                
                                # Second attempt: fix common JSON errors
                                try:
                                    cleaned_text = text.strip()
                                    # Fix trailing commas in objects
                                    cleaned_text = re.sub(r',\s*}', '}', cleaned_text)
                                    # Fix trailing commas in arrays
                                    cleaned_text = re.sub(r',\s*]', ']', cleaned_text)
                                    # Fix missing quotes around property names
                                    cleaned_text = re.sub(r'(\s*|{|,)([a-zA-Z0-9_]+)(\s*):', r'\1"\2"\3:', cleaned_text)
                                    parsed_json = json.loads(cleaned_text)
                                except json.JSONDecodeError as e:
                                    json_errors.append(f"JSON cleaning error: {e}")
                                    
                                    # Third attempt: extract JSON using regex
                                    try:
                                        import re
                                        json_matches = re.findall(r'{.*}', text, re.DOTALL)
                                        if json_matches:
                                            parsed_json = json.loads(json_matches[0])
                                        else:
                                            raise ValueError("No JSON object found in response")
                                    except Exception as e:
                                        json_errors.append(f"JSON extraction error: {e}")
                                        raise ValueError(f"Failed to parse JSON after multiple attempts: {json_errors}")

                            if not parsed_json:
                                raise ValueError("Failed to extract valid JSON from model response")

                            # Validate with Pydantic if a model was provided
                            if isinstance(response_schema, type) and issubclass(response_schema, BaseResponseSchema):
                                try:
                                    validated_data = response_schema.model_validate(parsed_json)
                                    return {
                                        "status": "success",
                                        "data": validated_data.model_dump()
                                    }
                                except ValidationError as e:
                                    # Detailed validation error with the schema
                                    error_details = str(e)
                                    logger.error(f"Schema validation error: {error_details}")
                                    
                                    # Try to construct a minimal valid response
                                    try:
                                        # Create minimal response with 'status' field
                                        minimal_data = {"status": "errors", "errors": [{"code": "schema_validation_error", "message": error_details}]}
                                        minimal_validated = response_schema.model_validate(minimal_data)
                                        
                                        return {
                                            "status": "error",
                                            "error": f"Schema validation error: {error_details}",
                                            "data": minimal_validated.model_dump()
                                        }
                                    except Exception as nested_e:
                                        logger.error(f"Failed to create minimal valid response: {nested_e}")
                                        raise ValueError(f"Response validation failed: {error_details}")

                            # If we're just using a dict schema, return the parsed JSON directly
                            return {
                                "status": "success",
                                "data": parsed_json
                            }
                        except Exception as e:
                            span.set_attribute("error", True)
                            span.set_attribute("error.message", str(e))
                            logger.error(f"Error processing model response: {e}")
                            raise ValueError(f"Failed to process model response: {e}")
                    
                    return {
                        "status": "success",
                        "data": response.text
                    }
                    
                except Exception as e:
                    last_error = e
                    attempt += 1
                    
                    if attempt <= self.max_retries:
                        delay = self._calculate_retry_delay(attempt)
                        logger.warning(f"Attempt {attempt} failed with error: {str(e)}. Retrying in {delay:.2f} seconds...")
                        time.sleep(delay)
                    else:
                        logger.error(f"All {self.max_retries} attempts failed. Last error: {str(last_error)}")
                        return {
                            "status": "error",
                            "error": str(last_error),
                            "data": None
                        }

def get_schema_model(task: str) -> Optional[Type[BaseResponseSchema]]:
    """
    Get the Pydantic model for the given task.
    
    Args:
        task: Task identifier (e.g., 'parsing', 'ps', 'cs', 'ka', 'role', 'scoring')
        
    Returns:
        Schema model class or None if not found
    """
    try:
        schema_model = SCHEMA_REGISTRY.get(task)
        if not schema_model:
            logger.warning(f"No schema model found for task: {task}")
        return schema_model
    except Exception as e:
        logger.error(f"Error retrieving schema model for task {task}: {e}")
        return None

# Remove the commented example usage since we'll use the function directly 