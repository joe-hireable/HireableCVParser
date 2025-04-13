import os
import json
import logging
import time
import re
from typing import Dict, Any, Optional, List, Type, Union
# Import for Vertex AI SDK
import google.cloud.aiplatform as aiplatform
# Import the specific GenerativeModel and other imports correctly
# so that mocking works properly in tests
from vertexai.generative_models import GenerativeModel
from vertexai.generative_models import Part
from vertexai.generative_models import GenerationConfig
from vertexai.generative_models import HarmCategory
from vertexai.generative_models import HarmBlockThreshold
from google.cloud import storage
from opentelemetry import trace
import base64
from pydantic import BaseModel, ValidationError
from models.schemas import BaseResponseSchema, SCHEMA_REGISTRY, StatusEnum, SeverityEnum
from enum import Enum

logger = logging.getLogger(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

class ErrorModel(BaseModel):
    """Model for error responses."""
    code: str
    message: str
    severity: SeverityEnum = SeverityEnum.ERROR

class GeminiClient:
    """Client for interacting with Gemini API via Vertex AI."""
    
    def __init__(self, project_id: str, location: str, model_name: str = "gemini-pro"):
        """
        Initialize the Gemini client using Vertex AI.

        Args:
            project_id: Google Cloud project ID
            location: Google Cloud region
            model_name: Name of the model to use

        Raises:
            ValueError: If initialization fails
        """
        self.project_id = project_id
        self.location = location
        self.model_name = model_name
        
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
        
        try:
            # Initialize Vertex AI
            aiplatform.init(project=project_id, location=location)
            # Initialize the Vertex AI GenerativeModel - using the import directly
            # so mocking works properly in test
            self.model = GenerativeModel(model_name=self.model_name)
            logging.info(f"Successfully initialized GeminiClient with Vertex AI SDK using model {model_name}")
        except Exception as e:
            error_msg = f"Failed to initialize GeminiClient with Vertex AI: {str(e)}"
            logging.error(error_msg)
            raise ValueError(error_msg) from e
    
    def _calculate_retry_delay(self, attempt: int) -> float:
        """Calculate exponential backoff delay."""
        delay = min(self.base_delay * (2 ** attempt), self.max_delay)
        return delay

    def _clean_json_response(self, response: str) -> str:
        """Clean JSON response from common issues."""
        # Remove markdown code blocks
        response = re.sub(r'```(?:json)?\n?(.*?)\n?```', r'\1', response, flags=re.DOTALL)
        
        # Fix unquoted keys
        response = re.sub(r'(\w+)(?=\s*:)', r'"\1"', response)
        
        # Remove trailing commas
        response = re.sub(r',(\s*[}\]])', r'\1', response)
        
        return response.strip()

    def _extract_json_from_text(self, text: str) -> str:
        """Extract JSON objects from text that might contain explanations."""
        # Try to find JSON objects in markdown code blocks first
        json_blocks = re.findall(r'```(?:json)?\n?(.*?)\n?```', text, flags=re.DOTALL)
        if json_blocks:
            return json_blocks[0]
        
        # Try to find JSON objects with curly braces, matching the pattern more carefully
        json_objects = re.findall(r'({[\s\S]*?})', text)
        
        if json_objects:
            # Try each JSON object until we find a valid one
            for json_obj in json_objects:
                try:
                    # Simple validation check
                    test_obj = json.loads(json_obj)
                    # If it parses successfully, return it
                    return json_obj
                except json.JSONDecodeError:
                    # Try the next one
                    continue
        
        # If no JSON blocks or valid objects found, return the original text
        return text

    def _process_schema_response(self, response_text: str, schema: Optional[Type[BaseModel]] = None) -> Dict[str, Any]:
        """Process and validate response against schema."""
        try:
            # Handle possible MagicMock
            if not isinstance(response_text, str):
                if hasattr(response_text, 'text'):
                    response_text = response_text.text
                else:
                    response_text = str(response_text)
            
            # Extract JSON from possibly longer text response
            extracted_text = self._extract_json_from_text(response_text)
            
            # Clean the response
            cleaned_response = self._clean_json_response(extracted_text)
            
            # Parse JSON
            data = json.loads(cleaned_response)
            
            # Validate against schema if provided
            if schema:
                validated_data = schema(**data)
                return {
                    "status": "success",
                    "data": validated_data.model_dump()
                }
            
            return {
                "status": "success",
                "data": data
            }
            
        except json.JSONDecodeError as e:
            return {
                "status": "error",
                "error": f"Failed to parse JSON response: {str(e)}",
                "data": {
                    "status": "errors",
                    "errors": [
                        ErrorModel(
                            code="json_parse_error",
                            message=str(e),
                            severity=SeverityEnum.ERROR
                        ).model_dump()
                    ]
                }
            }
        except ValidationError as e:
            return {
                "status": "error",
                "error": f"Schema validation error: {str(e)}",
                "data": {
                    "status": "errors",
                    "errors": [
                        ErrorModel(
                            code="schema_validation_error",
                            message=str(error),
                            severity=SeverityEnum.ERROR
                        ).model_dump()
                        for error in e.errors()
                    ]
                }
            }
        except Exception as e:
            return {
                "status": "error",
                "error": f"Failed to process model response: {str(e)}",
                "data": None
            }

    def generate_content(
        self,
        prompt: Union[str, List[Part]],
        *,
        response_schema: Optional[Type[BaseModel]] = None,
        file_uri: Optional[str] = None,
        mime_type: Optional[str] = None,
        system_prompt: Optional[str] = None,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_output_tokens: Optional[int] = None,
        top_p: Optional[float] = None,
        top_k: Optional[int] = None,
        config: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generate content using the Gemini model via Vertex AI.

        Args:
            prompt: Text prompt or list of Part objects
            response_schema: Optional Pydantic model for response validation
            file_uri: Optional GCS URI for file input
            mime_type: Optional MIME type for file input
            system_prompt: Optional system prompt
            model: Optional model override
            temperature: Optional temperature override
            max_output_tokens: Optional max tokens override
            top_p: Optional top_p override
            top_k: Optional top_k override
            config: Optional complete generation config override

        Returns:
            Dict containing status and response data
        """
        with self.tracer.start_as_current_span("generate_content") as span:
            try:
                # Use the model name specified in the call, or the default
                target_model = self.model
                if model:
                    target_model = GenerativeModel(model_name=model)

                # Prepare content parts
                content_parts = []
                
                # Add system prompt if provided
                if system_prompt:
                    content_parts.append(Part.from_text(system_prompt))
                
                # Handle file input
                if file_uri:
                    if not mime_type:
                        mime_type = "application/octet-stream"
                    content_parts.append(Part.from_uri(file_uri, mime_type=mime_type))
                
                # Add main prompt
                if isinstance(prompt, str):
                    content_parts.append(Part.from_text(prompt))
                elif isinstance(prompt, list):
                    content_parts.extend(prompt)
                else:
                    content_parts.append(prompt)

                # Prepare generation config
                generation_config = {
                    "temperature": temperature or self.default_config["temperature"],
                    "top_p": top_p or self.default_config["top_p"],
                    "top_k": top_k or self.default_config["top_k"],
                    "max_output_tokens": max_output_tokens or self.default_config["max_output_tokens"],
                    "candidate_count": self.default_config["candidate_count"]
                }
                
                # Override with custom config if provided
                if config:
                    generation_config.update(config)

                last_exception = None
                # Generate content with retries
                for attempt in range(self.max_retries):
                    try:
                        response = target_model.generate_content(
                            content_parts,
                            generation_config=generation_config,
                            safety_settings={
                                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE
                            }
                        )
                        
                        # Process the response
                        if response_schema:
                            return self._process_schema_response(response.text, response_schema)
                        
                        return {
                            "status": "success",
                            "data": {"text": response.text}
                        }
                        
                    except Exception as e:
                        last_exception = e
                        # Don't break early for retries
                        if attempt == self.max_retries - 1:
                            break
                        
                        delay = self._calculate_retry_delay(attempt)
                        logging.warning(f"Attempt {attempt + 1} failed, retrying in {delay} seconds: {str(e)}")
                        time.sleep(delay)
                
                # If we get here, all retries failed
                if last_exception:
                    error_msg = f"Failed to generate content: {str(last_exception)}"
                    logging.error(error_msg)
                    return {
                        "status": "error",
                        "error": error_msg,
                        "data": None
                    }
                else:
                    # This should never happen if there was at least one attempt
                    error_msg = "No response after maximum retries"
                    logging.error(error_msg)
                    return {
                        "status": "error",
                        "error": error_msg,
                        "data": None
                    }
                        
            except Exception as e:
                error_msg = f"Failed to generate content: {str(e)}"
                logging.error(error_msg)
                return {
                    "status": "error",
                    "error": error_msg,
                    "data": None
                }
                
    def _get_model(self):
        """Return the current model instance."""
        return self.model

def get_schema_model(task: str) -> Optional[Type[BaseResponseSchema]]:
    """Get the appropriate response schema model for a given task."""
    if task is None:
        return None
        
    try:
        # Use dictionary get method instead of attribute access for test mocking
        schema = None
        if task.lower() in SCHEMA_REGISTRY:
            schema = SCHEMA_REGISTRY[task.lower()]
        return schema
    except Exception as e:
        logging.error(f"Error getting schema model for task '{task}': {str(e)}")
        return None 