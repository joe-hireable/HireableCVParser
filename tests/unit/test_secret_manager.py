import pytest
from unittest.mock import patch, MagicMock
from utils.secret_manager import SecretManagerClient
from google.api_core.exceptions import NotFound


class TestSecretManagerClient:
    """Test cases for SecretManagerClient."""

    @pytest.fixture
    def secret_manager_client(self):
        """Create a SecretManagerClient instance for testing."""
        # Mock the Secret Manager client
        with patch("utils.secret_manager.secretmanager.SecretManagerServiceClient") as mock_sm_client:
            mock_client = MagicMock()
            mock_sm_client.return_value = mock_client
            return SecretManagerClient(project_id="test-project")
    
    @patch("utils.secret_manager.secretmanager.SecretManagerServiceClient")
    def test_init(self, mock_sm_client):
        """Test SecretManagerClient initialization."""
        # Create a client
        client = SecretManagerClient(project_id="test-project")
        
        # Verify secretmanager.SecretManagerServiceClient was called
        mock_sm_client.assert_called_once()
        
        # Check that the client has the expected attributes
        assert hasattr(client, "client")
        assert hasattr(client, "project_id")
        assert client.project_id == "test-project"
    
    def test_get_secret(self, secret_manager_client):
        """Test get_secret method."""
        # Setup mock for secret access
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.payload.data = b"test-secret-value"
        mock_client.access_secret_version.return_value = mock_response
        secret_manager_client.client = mock_client
        
        # Call the method
        result = secret_manager_client.get_secret("api-key")
        
        # Verify client.access_secret_version was called with correct parameters
        secret_path = f"projects/test-project/secrets/api-key/versions/latest"
        mock_client.access_secret_version.assert_called_once_with(request={"name": secret_path})
        
        # Check returned result
        assert result == "test-secret-value"
    
    def test_get_secret_nonexistent(self, secret_manager_client):
        """Test get_secret method with a non-existent secret."""
        # Setup mock to raise NotFound exception
        mock_client = MagicMock()
        mock_client.access_secret_version.side_effect = NotFound("Secret not found")
        secret_manager_client.client = mock_client
        
        # Call the method
        result = secret_manager_client.get_secret("nonexistent-secret")
        
        # Verify the result is None for non-existent secrets
        assert result is None
        
        # Verify client.access_secret_version was called
        secret_path = f"projects/test-project/secrets/nonexistent-secret/versions/latest"
        mock_client.access_secret_version.assert_called_once_with(request={"name": secret_path})
    
    # TODO: Add more tests for different secret types
    # TODO: Add tests for caching behavior if implemented 