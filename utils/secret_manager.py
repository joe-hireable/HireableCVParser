"""Utility for interacting with Google Cloud Secret Manager."""

import json
import logging
from typing import Dict, Any, Optional, Union

from google.cloud import secretmanager
from google.api_core.exceptions import NotFound

logger = logging.getLogger(__name__)

class SecretManagerClient:
    """Client for interacting with Google Cloud Secret Manager."""
    
    def __init__(self, project_id: str):
        """
        Initialize the Secret Manager client.
        
        Args:
            project_id: Google Cloud project ID
        """
        self.project_id = project_id
        self.client = secretmanager.SecretManagerServiceClient()
        self._cache: Dict[str, Any] = {}
        
    def get_secret(self, secret_id: str, version_id: str = "latest") -> Optional[str]:
        """
        Get a secret from Secret Manager.
        
        Args:
            secret_id: ID of the secret
            version_id: Version of the secret (default: latest)
            
        Returns:
            Secret payload as a string, or None if not found
        """
        cache_key = f"{secret_id}:{version_id}"
        if cache_key in self._cache:
            return self._cache[cache_key]
            
        try:
            # Build the resource name
            name = f"projects/{self.project_id}/secrets/{secret_id}/versions/{version_id}"
            
            # Access the secret version
            response = self.client.access_secret_version(request={"name": name})
            
            # Extract the payload
            payload = response.payload.data.decode("UTF-8")
            
            # Cache the result
            self._cache[cache_key] = payload
            
            return payload
        except NotFound:
            logger.warning(f"Secret {secret_id} (version {version_id}) not found")
            return None
        except Exception as e:
            logger.error(f"Error getting secret {secret_id}: {e}")
            return None
            
    def get_prompt(self, task: str, prompt_type: str, prefix: str) -> Optional[str]:
        """
        Get a prompt from Secret Manager.
        
        Args:
            task: Task identifier (parsing, ps, cs, etc.)
            prompt_type: Type of prompt (system, user)
            prefix: Secret name prefix
            
        Returns:
            Prompt as a string, or None if not found
        """
        if prompt_type == "system":
            secret_id = f"{prefix}system-prompt"
        else:
            secret_id = f"{prefix}{task}-user-prompt"
            
        return self.get_secret(secret_id)
        
    def get_schema(self, task: str, prefix: str) -> Optional[Dict[str, Any]]:
        """
        Get a schema from Secret Manager.
        
        Args:
            task: Task identifier (parsing, ps, cs, etc.)
            prefix: Secret name prefix
            
        Returns:
            Schema as a dictionary, or None if not found
        """
        secret_id = f"{prefix}{task}-schema"
        schema_json = self.get_secret(secret_id)
        
        if schema_json:
            try:
                return json.loads(schema_json)
            except json.JSONDecodeError as e:
                logger.error(f"Error parsing schema JSON for {task}: {e}")
                return None
        
        return None
        
    def get_examples(self, task: str, prefix: str) -> Optional[str]:
        """
        Get few-shot examples from Secret Manager.
        
        Args:
            task: Task identifier (parsing, ps, cs, etc.)
            prefix: Secret name prefix
            
        Returns:
            Examples as a string, or None if not found
        """
        secret_id = f"{prefix}{task}-examples"
        return self.get_secret(secret_id) 