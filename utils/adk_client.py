"""Utility for interacting with Google Agent Development Kit (ADK)."""

import json
import logging
from typing import Dict, Any, Optional, List, Type
from unittest.mock import MagicMock
try:
    import google.adk as adk
    ADK_AVAILABLE = True
except ImportError:
    ADK_AVAILABLE = False
    # Create a mock ADK module for testing that better matches real ADK behavior
    class MockSession:
        def __init__(self, parameters):
            self.parameters = parameters
            self.response = {
                "status": "success",
                "data": {
                    "firstName": "John",
                    "surname": "Doe",
                    "email": "john.doe@example.com"
                }
            }
            
        def execute(self):
            return MagicMock(
                structured_response=json.dumps(self.response)
            )
            
    class MockAgent:
        def __init__(self, **kwargs):
            self.agent_name = kwargs.get('agent_name')
            self.session = None
            
        def start_session(self, parameters):
            self.session = MockSession(parameters)
            return self.session
            
        def cleanup(self):
            if self.session:
                self.session = None
                
    class MockADK:
        def __init__(self):
            self.Agent = MockAgent
            
    adk = MockADK()

from opentelemetry import trace
from pydantic import ValidationError
from models.schemas import SCHEMA_REGISTRY, BaseResponseSchema
from utils.document_processor import DocumentProcessor

logger = logging.getLogger(__name__)

class ADKClient:
    """Client for interacting with Google Agent Development Kit."""
    
    def __init__(self, agent_location: str):
        """
        Initialize the ADK client.
        
        Args:
            agent_location: Full location path to the ADK agent
        """
        self.agent_location = agent_location
        self.tracer = trace.get_tracer(__name__)
        self.agent = None
        # Initialize agent immediately
        try:
            # Use the correct initialization format based on the documentation
            self.agent = adk.Agent(
                agent_name=self.agent_location
            )
            if not ADK_AVAILABLE:
                logger.warning("ADK is not available. Using mock implementation.")
            else:
                logger.info(f"Initialized ADK agent: {self.agent_location}")
        except Exception as e:
            logger.error(f"Failed to initialize ADK agent: {e}")
            self.agent = None
        
    def initialize_agent(self):
        """Initialize the ADK agent if it doesn't exist."""
        if not self.agent:
            try:
                # Use the correct initialization format based on the documentation
                self.agent = adk.Agent(
                    agent_name=self.agent_location
                )
                if not ADK_AVAILABLE:
                    logger.warning("ADK is not available. Using mock implementation.")
                else:
                    logger.info(f"Initialized ADK agent: {self.agent_location}")
                return True
            except Exception as e:
                logger.error(f"Failed to initialize ADK agent: {e}")
                return False
        return True
    
    def cleanup(self):
        """Close the ADK agent."""
        if self.agent:
            self.agent = None
    
    def process_cv(
        self, 
        cv_content: str, 
        task: str,
        jd_content: Optional[str] = None,
        section: Optional[str] = None,
        config: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Process a CV using the ADK agent.
        
        Args:
            cv_content: CV text content
            task: Task to perform (parsing, ps, cs, ka, role, scoring)
            jd_content: Optional job description content
            section: Optional section to focus on
            config: Optional configuration parameters
            
        Returns:
            Processing result as a dictionary
        """
        with self.tracer.start_as_current_span("adk_process_cv") as span:
            span.set_attribute("task", task)
            
            # Handle None input
            if cv_content is None:
                logger.error("CV content cannot be None")
                return {
                    "status": "error",
                    "error": "CV content cannot be None",
                    "data": None
                }
                
            span.set_attribute("cv.length", len(cv_content))
            if jd_content:
                span.set_attribute("jd.length", len(jd_content))
            if section:
                span.set_attribute("section", section)
                
            try:
                # Check if agent exists, try to initialize if not
                if not self.agent and not self.initialize_agent():
                    return {
                        "status": "error",
                        "error": "Failed to initialize ADK agent",
                        "data": None
                    }
                
                # Get the appropriate schema model for validation
                schema_model = self._get_schema_model(task)
                
                # Create parameters for ADK session
                parameters = {
                    "task": task,
                    "cv_content": cv_content,
                    "jd_content": jd_content or "",
                    "section": section or ""
                }
                
                if config:
                    parameters.update(config)
                    
                # Start ADK session
                session = self.agent.start_session(parameters)
                
                # Get result from session
                result = session.execute()
                
                # Extract structured data from result
                try:
                    # Log the raw response for debugging
                    response_text = result.structured_response
                    logger.debug(f"Raw ADK response: {response_text[:1000]}...")
                    
                    # Parse JSON response
                    data = json.loads(response_text)
                    
                    # Validate against schema if available
                    if schema_model:
                        try:
                            # Extract the data part from the response
                            response_data = data.get("data", {})
                            
                            # For mock schema instances that may have an instance, call directly
                            # Otherwise assume it's a class and instantiate it
                            if hasattr(schema_model, 'model_validate'):
                                validated_data = schema_model.model_validate(response_data)
                            else:
                                # Create a new instance of the schema model class
                                validated_data = schema_model().model_validate(response_data)
                            
                            # Handle both cases: model_dump method or direct dict return
                            if hasattr(validated_data, 'model_dump'):
                                return {
                                    "status": "success",
                                    "data": validated_data.model_dump()
                                }
                            else:
                                # Direct return if it's a plain object with no model_dump
                                return {
                                    "status": "success",
                                    "data": validated_data
                                }
                        except Exception as e:
                            # Detailed validation error
                            error_details = str(e)
                            logger.error(f"ADK processing error: {error_details}")
                            
                            # Create error response
                            error_response = {
                                "status": "error",
                                "error": f"Schema validation error: {error_details}",
                                "data": data  # Include the unvalidated data for inspection
                            }
                            
                            # Try to create a minimal valid response if possible
                            try:
                                minimal_data = {"status": "errors", "errors": [{"code": "schema_validation_error", "message": error_details}]}
                                if hasattr(schema_model, 'model_validate'):
                                    validated_minimal = schema_model.model_validate(minimal_data)
                                else:
                                    validated_minimal = schema_model().model_validate(minimal_data)
                                
                                if hasattr(validated_minimal, 'model_dump'):
                                    error_response["data"] = validated_minimal.model_dump()
                                else:
                                    error_response["data"] = validated_minimal
                            except Exception:
                                pass  # Keep the original data if we can't create a valid minimal response
                                
                            return error_response
                    
                    # If no schema or validation passed, return the data directly
                    return {
                        "status": "success",
                        "data": data.get("data", data)
                    }
                except json.JSONDecodeError as e:
                    span.set_attribute("error", True)
                    span.set_attribute("error.message", str(e))
                    logger.error(f"Failed to parse ADK JSON response: {e}")
                    
                    # Try to extract any JSON-like content using regex
                    import re
                    json_matches = re.findall(r'{.*}', response_text, re.DOTALL)
                    if json_matches:
                        try:
                            extracted_json = json.loads(json_matches[0])
                            logger.info("Successfully extracted JSON using regex fallback")
                            return {
                                "status": "success", 
                                "data": extracted_json.get("data", extracted_json)
                            }
                        except Exception:
                            pass
                    
                    return {
                        "status": "error",
                        "error": f"Invalid JSON response: {e}",
                        "data": response_text  # Return the text response as fallback
                    }
                    
            except Exception as e:
                span.set_attribute("error", True)
                span.set_attribute("error.message", str(e))
                logger.error(f"ADK processing error: {e}")
                return {
                    "status": "error",
                    "error": str(e),
                    "data": None
                }
    
    def _get_schema_model(self, task: str) -> Optional[Type[BaseResponseSchema]]:
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