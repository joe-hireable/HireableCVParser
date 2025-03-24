import os
import json
import logging
from typing import Dict, Any, Optional, List
from google.oauth2 import service_account
from config import VERTEX_AI_ENABLED
from google.auth.exceptions import DefaultCredentialsError
from google import genai
from google.genai.types import HttpOptions, Part, GenerateContentConfig
from google.cloud import aiplatform


logger = logging.getLogger(__name__)

class GeminiClient:
    """Client for interacting with Gemini API via Google Generative AI or Vertex AI."""
    
    def __init__(self, project_id: str, location: str = "europe-west2", key_path: Optional[str] = None):
        """
        Initialize the Gemini client.
        
        Args:
            project_id: Google Cloud project ID
            location: Google Cloud region (default: europe-west2 for UK)
            key_path: Path to service account JSON key file (optional)
            
        Raises:
            FileNotFoundError: If the key file doesn't exist
            ValueError: If the key file is invalid
        """
        self.project_id = project_id
        self.location = location
        
        try:
            if key_path and os.path.exists(key_path):
                # Use service account key file
                credentials = service_account.Credentials.from_service_account_file(key_path)
                
                # Initialize Vertex AI with explicit credentials
                aiplatform.init(
                    project=project_id,
                    location=location,
                    credentials=credentials
                )
                
                # Configure Gemini with credentials
                genai.configure(credentials=credentials)
                
                logger.info(f"Initialized Gemini client for project {project_id} using service account key")
            else:
                # Fall back to ADC
                aiplatform.init(project=project_id, location=location)
                logger.info(f"Initialized Gemini client for project {project_id} using ADC")
                
        except FileNotFoundError:
            logger.error(f"Service account key file not found: {key_path}")
            raise
        except Exception as e:
            logger.error(f"Failed to initialize Gemini client: {str(e)}")
            raise
        
        # Default generation config
        self.default_config = {
            "temperature": 0.5,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 8192,
            "candidate_count": 1
        }
        
        # Model name for Gemini 2.0 Flash
        self.model_name = "gemini-2.0-flash"
        
        # Initialize the appropriate client based on configuration
        self.use_vertex_ai = VERTEX_AI_ENABLED
        
        if self.use_vertex_ai:
            # Initialize Vertex AI
            aiplatform.init(project=project_id, location=location)
        else:
            # Initialize Google Generative AI
            # API key should be set via environment variable GOOGLE_API_KEY or explicitly
            api_key = os.environ.get("GOOGLE_API_KEY")
            if api_key:
                genai.configure(api_key=api_key)
        
        logger.info(f"Initialized Gemini client with project ID {project_id} in {location}")
    
    def generate_content(
        self,
        prompt: str,
        schema: Optional[Dict[str, Any]] = None,
        system_prompt: Optional[str] = None,
        generation_config: Optional[Dict[str, Any]] = None,
        file_uri: Optional[str] = None,
        mime_type: str = "application/pdf"
    ) -> Dict[str, Any]:
        
        try:
            # Create a client with Vertex AI integration
            client = genai.Client(
                vertexai=True,
                project=self.project_id,
                location=self.location
            )
            
            # Prepare generation config
            config_params = self.default_config.copy()
            if generation_config:
                config_params.update(generation_config)
            
            # Prepare content parts based on whether we have a file
            contents = []
            if file_uri:
                # File-based content with optional text prompt
                contents.append({"file_uri": file_uri, "mime_type": mime_type})
                if prompt:
                    contents.append(prompt)
            else:
                # Text-only content
                contents.append(prompt)
            
            # Generate content directly with the models API
            response = client.models.generate_content(
                model=self.model_name,
                contents=contents,
                generation_config=config_params,
                system_instruction=system_prompt if system_prompt else None,
                response_mime_type="application/json" if schema else None,
                response_schema=schema if schema else None
            )
            
            # Handle schema-based responses
            if schema:
                try:
                    # Clean and parse JSON response
                    text = response.text
                    if text.startswith("```json"):
                        text = text[7:]
                    if text.endswith("```"):
                        text = text[:-3]
                    parsed_json = json.loads(text.strip())
                    return {
                        "status": "success",
                        "data": parsed_json
                    }
                except json.JSONDecodeError as e:
                    logger.error(f"Failed to parse JSON response: {e}")
                    return {
                        "status": "error",
                        "error": f"Invalid JSON response: {e}",
                        "data": response.text
                    }
            
            return {
                "status": "success",
                "data": response.text
            }
            
        except Exception as e:
            logger.error(f"Error generating content with Gemini: {e}")
            return {
                "status": "error",
                "error": str(e),
                "data": None
            } 