from dataclasses import dataclass, field
from typing import Optional, List
from google.oauth2 import service_account
from google.auth.credentials import Credentials
import os
from utils.result import Result

@dataclass
class CredentialConfig:
    """Configuration for credential management."""
    key_path: Optional[str] = None
    project_id: Optional[str] = None
    location: str = "europe-west2"
    scopes: List[str] = field(default_factory=list)

class CredentialProvider:
    """Centralized credential management."""
    
    def __init__(self, config: CredentialConfig):
        self.config = config
        self._credentials: Optional[Credentials] = None
    
    @property
    def credentials(self) -> Optional[Credentials]:
        """Lazy loading of credentials."""
        if self._credentials is None:
            self._credentials = self._load_credentials()
        return self._credentials
    
    def _load_credentials(self) -> Optional[Credentials]:
        """Load credentials from key file or ADC."""
        try:
            if self.config.key_path and os.path.exists(self.config.key_path):
                return service_account.Credentials.from_service_account_file(
                    self.config.key_path,
                    scopes=self.config.scopes
                )
            return None  # Fall back to ADC
        except Exception as e:
            logger.error(f"Failed to load credentials: {e}")
            return None 

    @classmethod
    def get_credentials(cls, config: CredentialConfig) -> Result[Credentials]:
        try:
            if config.key_path and os.path.exists(config.key_path):
                return Result.ok(
                    service_account.Credentials.from_service_account_file(
                        config.key_path,
                        scopes=config.scopes
                    )
                )
            return Result.ok(None)  # Fall back to ADC
        except Exception as e:
            return Result.err(f"Failed to load credentials: {str(e)}") 