"""Client for interacting with Gemini API via Google Generative AI or Vertex AI."""

import os
import json
import logging
from typing import Dict, Any, Optional, List
from google.auth import default
from config import VERTEX_AI_ENABLED
from google.auth.exceptions import DefaultCredentialsError
from google import generativeai as genai
from google.cloud import aiplatform

logger = logging.getLogger(__name__)

class GeminiClient:
    """Client for interacting with Gemini API via Google Generative AI or Vertex AI."""
    
    def __init__(self, project_id: str, location: str = "europe-west2"):
        """
        Initialize the Gemini client.
        
        Args:
            project_id: Google Cloud project ID
            location: Google Cloud region (default: europe-west2 for UK)
            
        Raises:
            DefaultCredentialsError: If no credentials are found
        """
        self.project_id = project_id
        self.location = location
        
        try:
            # Get default credentials
            credentials, project = default()
            if not credentials:
                raise DefaultCredentialsError("No credentials found")
            
            # Initialize Vertex AI with explicit credentials
            aiplatform.init(
                project=project_id,
                location=location,
                credentials=credentials
            )
            
            # Configure Gemini with credentials
            genai.configure(credentials=credentials)
            
            logger.info(f"Initialized Gemini client for project {project_id} using ADC")
        except DefaultCredentialsError as e:
            logger.error("Failed to initialize Gemini client: No credentials found")
            raise
        except Exception as e:
            logger.error(f"Failed to initialize Gemini client: {str(e)}")
            raise
        
        # Default generation config
        self.default_config = {
            "temperature": 0.2,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 8192,
            "candidate_count": 1
        }
        
        # Model name for Gemini 2.0 Flash
        self.model_name = "gemini-2.0-flash-lite"
        
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
        generation_config: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generate content using Gemini model.
        
        Args:
            prompt: Main prompt text
            schema: Optional JSON schema for structured output
            system_prompt: Optional system prompt for context
            generation_config: Optional custom generation configuration
            
        Returns:
            Generated content response
        """
        try:
            # Use the appropriate API based on configuration
            if self.use_vertex_ai:
                return self._generate_with_vertex_ai(
                    prompt=prompt,
                    schema=schema,
                    system_prompt=system_prompt,
                    generation_config=generation_config
                )
            else:
                return self._generate_with_generative_ai(
                    prompt=prompt,
                    schema=schema,
                    system_prompt=system_prompt,
                    generation_config=generation_config
                )
                
        except Exception as e:
            logger.error(f"Error generating content with Gemini: {e}")
            return {
                "status": "error",
                "error": str(e),
                "data": None
            }
    
    def _generate_with_generative_ai(
        self,
        prompt: str,
        schema: Optional[Dict[str, Any]] = None,
        system_prompt: Optional[str] = None,
        generation_config: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Generate content using the Google Generative AI library"""
        try:
            # Initialize model
            model = genai.GenerativeModel(self.model_name)
            
            # Prepare generation config
            config = self.default_config.copy()
            if generation_config:
                config.update(generation_config)
            
            # Create content
            messages = []
            if system_prompt:
                messages.append({"role": "system", "parts": [system_prompt]})
            
            messages.append({"role": "user", "parts": [prompt]})
            
            # Generate content
            response = model.generate_content(
                messages,
                generation_config=config,
                response_mime_type="application/json" if schema else None,
            )
            
            # Process response
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
            logger.error(f"Error generating content with Google Generative AI: {e}")
            return {
                "status": "error",
                "error": str(e),
                "data": None
            }
    
    def _generate_with_vertex_ai(
        self,
        prompt: str,
        schema: Optional[Dict[str, Any]] = None,
        system_prompt: Optional[str] = None,
        generation_config: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Generate content using Vertex AI (for backward compatibility)"""
        try:
            # Import Vertex AI components here to avoid issues if Vertex AI is not available
            from vertexai.preview.generative_models import GenerativeModel
            from vertexai.preview.generative_models import Part, Content
            from vertexai.preview.generative_models import GenerationConfig as VertexGenerationConfig
            
            # Initialize model
            model = GenerativeModel(self.model_name)
            
            # Prepare generation config
            config_params = self.default_config.copy()
            if generation_config:
                config_params.update(generation_config)
                
            config = VertexGenerationConfig(**config_params)
            
            # Prepare content parts
            parts = [Part.from_text(prompt)]
            
            # Create content with role
            contents = [Content(
                role="user",
                parts=parts
            )]
            
            # Add system prompt if provided
            if system_prompt:
                contents.insert(0, Content(
                    role="system",
                    parts=[Part.from_text(system_prompt)]
                ))
            
            # Generate content
            response = model.generate_content(
                contents=contents,
                generation_config=config,
            )
            
            # Process response based on schema
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
            logger.error(f"Error generating content with Vertex AI: {e}")
            return {
                "status": "error",
                "error": str(e),
                "data": None
            }
    
    def generate_from_file(
        self,
        file_uri: str,
        prompt: Optional[str] = None,
        schema: Optional[Dict[str, Any]] = None,
        system_prompt: Optional[str] = None,
        generation_config: Optional[Dict[str, Any]] = None,
        mime_type: str = "application/pdf"
    ) -> Dict[str, Any]:
        """
        Generate content from a file using Gemini model.
        
        Args:
            file_uri: GCS URI of the file (gs://bucket/path)
            prompt: Optional text prompt
            schema: Optional JSON schema for structured output
            system_prompt: Optional system prompt for context
            generation_config: Optional custom generation configuration
            mime_type: MIME type of the file
            
        Returns:
            Generated content response
        """
        try:
            # File-based generation is only supported in Vertex AI currently
            # Fallback to Vertex AI implementation for file operations
            from vertexai.preview.generative_models import GenerativeModel
            from vertexai.preview.generative_models import Part, Content
            from vertexai.preview.generative_models import GenerationConfig as VertexGenerationConfig
            
            # Initialize model
            model = GenerativeModel(self.model_name)
            
            # Prepare generation config
            config_params = self.default_config.copy()
            if generation_config:
                config_params.update(generation_config)
                
            config = VertexGenerationConfig(**config_params)
            
            # Prepare content parts
            parts = [Part.from_uri(file_uri, mime_type=mime_type)]
            if prompt:
                parts.append(Part.from_text(prompt))
            
            # Create content with role
            contents = [Content(
                role="user",
                parts=parts
            )]
            
            # Add system prompt if provided
            if system_prompt:
                contents.insert(0, Content(
                    role="system",
                    parts=[Part.from_text(system_prompt)]
                ))
            
            # Generate content
            response = model.generate_content(
                contents=contents,
                generation_config=config,
            )
            
            # Process response based on schema
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
            logger.error(f"Error generating content from file with Gemini: {e}")
            return {
                "status": "error",
                "error": str(e),
                "data": None
            }
    
    def generate_text(
        self,
        prompt: str,
        schema: Optional[Dict[str, Any]] = None,
        system_instruction: Optional[str] = None,
        generation_config: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Alias for generate_content with a more intuitive name.
        
        Args:
            prompt: Main prompt text
            schema: Optional JSON schema for structured output
            system_instruction: Optional system instruction for context (alias for system_prompt)
            generation_config: Optional custom generation configuration
            
        Returns:
            Generated content response
        """
        return self.generate_content(
            prompt=prompt,
            schema=schema,
            system_prompt=system_instruction,
            generation_config=generation_config
        ) 