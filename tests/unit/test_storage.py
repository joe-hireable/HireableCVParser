import pytest
from unittest.mock import patch, MagicMock
from utils.storage import StorageClient


class TestStorageClient:
    """Test cases for StorageClient."""

    @pytest.fixture
    def storage_client(self):
        """Create a StorageClient instance for testing."""
        with patch('utils.storage.storage.Client') as mock_client:
            mock_bucket = MagicMock()
            mock_client.return_value.bucket.return_value = mock_bucket
            return StorageClient(bucket_name="test-bucket")

    def test_init(self, storage_client):
        """Test StorageClient initialization."""
        assert storage_client.bucket_name == "test-bucket"
        assert hasattr(storage_client, "storage_client")
        assert hasattr(storage_client, "bucket")

    def test_upload_file(self, storage_client):
        """Test upload_file method."""
        # Setup mock bucket and blob
        mock_blob = MagicMock()
        mock_bucket = MagicMock()
        mock_bucket.blob.return_value = mock_blob
        storage_client.bucket = mock_bucket

        # Test file upload
        content = "Test content"
        folder = "test-folder"
        result = storage_client.upload_file(content, folder)

        # Verify mocks were called
        mock_bucket.blob.assert_called_once()
        mock_blob.upload_from_string.assert_called_once_with(content)

        # Check returned URI format
        assert result.startswith("gs://test-bucket/test-folder/")
        assert result.endswith(".txt")

    def test_download_file(self, storage_client):
        """Test download_file method."""
        # Setup mock bucket and blob
        mock_blob = MagicMock()
        mock_blob.download_as_text.return_value = "Downloaded content"
        
        # Setup storage client with proper mocking
        storage_client.bucket = MagicMock()
        storage_client.bucket.blob.return_value = mock_blob
        storage_client.storage_client = MagicMock()
        storage_client.storage_client.bucket.return_value = storage_client.bucket

        # Test file download
        gcs_uri = "gs://test-bucket/test-file.txt"
        result = storage_client.download_file(gcs_uri)

        # Verify mocks were called
        storage_client.bucket.blob.assert_called_once_with("test-file.txt")
        mock_blob.download_as_text.assert_called_once()

        # Check returned content
        assert result == "Downloaded content"

    def test_download_file_invalid_uri(self, storage_client):
        """Test download_file method with invalid GCS URI."""
        # Test with invalid URI
        result = storage_client.download_file("invalid-uri")

        # Check that None is returned
        assert result is None

    def test_save_bytes_to_gcs(self, storage_client):
        """Test save_bytes_to_gcs method."""
        # Setup mock bucket and blob
        mock_blob = MagicMock()
        mock_bucket = MagicMock()
        mock_bucket.blob.return_value = mock_blob
        storage_client.bucket = mock_bucket

        # Test bytes upload
        file_bytes = b"Test file bytes"
        gcs_path = "test-folder/test-file.txt"
        content_type = "text/plain"
        result = storage_client.save_bytes_to_gcs(file_bytes, gcs_path, content_type)

        # Verify mocks were called
        mock_bucket.blob.assert_called_once_with(gcs_path)
        mock_blob.upload_from_string.assert_called_once_with(file_bytes, content_type=content_type)

        # Check returned GCS URI
        assert result == f"gs://{storage_client.bucket_name}/{gcs_path}"

    def test_read_file(self, storage_client):
        """Test read_file method."""
        # Setup mock bucket and blob
        mock_blob = MagicMock()
        mock_blob.download_as_text.return_value = "File content"
        mock_bucket = MagicMock()
        mock_bucket.blob.return_value = mock_blob
        storage_client.bucket = mock_bucket

        # Test file read
        path = "test-folder/test-file.txt"
        result = storage_client.read_file(path)

        # Verify mocks were called
        mock_bucket.blob.assert_called_once_with(path)
        mock_blob.download_as_text.assert_called_once()

        # Check returned content
        assert result == "File content"

    def test_write_file(self, storage_client):
        """Test write_file method."""
        # Setup mock bucket and blob
        mock_blob = MagicMock()
        mock_bucket = MagicMock()
        mock_bucket.blob.return_value = mock_blob
        storage_client.bucket = mock_bucket

        # Test file write
        path = "test-files/test-file.txt"
        content = "Test content"
        result = storage_client.write_file(path, content)

        # Verify mocks were called
        mock_bucket.blob.assert_called_once_with(path)
        mock_blob.upload_from_string.assert_called_once_with(content)

        # Check returned result
        assert result is True

    def test_delete_file(self, storage_client):
        """Test delete_file method."""
        # Setup mock bucket and blob
        mock_blob = MagicMock()
        mock_bucket = MagicMock()
        mock_bucket.blob.return_value = mock_blob
        storage_client.bucket = mock_bucket
        
        # Call the method
        storage_client.delete_file("test-files/test-file.txt")
        
        # Verify mocks were called
        mock_bucket.blob.assert_called_once_with("test-files/test-file.txt")
        mock_blob.delete.assert_called_once()
    
    # TODO: Add tests for error handling
    # TODO: Add tests for list_files method
    # TODO: Add tests for file existence checking 