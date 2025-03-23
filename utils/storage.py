import logging
from google.cloud import storage
from typing import Optional
import os
from google.oauth2 import service_account

logger = logging.getLogger(__name__)

class StorageClient:
    """Client for interacting with Google Cloud Storage."""
    
    def __init__(self, bucket_name: str, key_path: Optional[str] = None):
        """
        Initialize the Storage client.
        
        Args:
            bucket_name: Name of the GCS bucket to use
            key_path: Path to service account JSON key file (optional)
            
        Raises:
            FileNotFoundError: If the key file doesn't exist
            ValueError: If the key file is invalid
        """
        self.bucket_name = bucket_name
        
        try:
            if key_path and os.path.exists(key_path):
                # Use service account key file
                credentials = service_account.Credentials.from_service_account_file(key_path)
                self.storage_client = storage.Client(credentials=credentials)
                logger.info(f"Initialized Storage client for bucket {bucket_name} using service account key")
            else:
                # Fall back to ADC if no key provided or file doesn't exist
                self.storage_client = storage.Client()
                logger.info(f"Initialized Storage client for bucket {bucket_name} using ADC")
                
            self.bucket = self.storage_client.bucket(bucket_name)
            
        except FileNotFoundError:
            logger.error(f"Service account key file not found: {key_path}")
            raise
        except Exception as e:
            logger.error(f"Failed to initialize Storage client: {str(e)}")
            raise
    
    def upload_file(self, content: str, folder: str) -> Optional[str]:
        """
        Upload content to GCS.
        
        Args:
            content: Content to upload
            folder: Folder in bucket (e.g., 'cvs' or 'jds')
            
        Returns:
            GCS URI of the uploaded file or None if upload fails
        """
        try:
            # Generate a unique filename
            filename = f"{folder}/{os.urandom(8).hex()}.txt"
            
            # Create a blob and upload the content
            blob = self.bucket.blob(filename)
            blob.upload_from_string(content)
            
            # Return the GCS URI
            gcs_uri = f"gs://{self.bucket_name}/{filename}"
            logger.info(f"Successfully uploaded file to {gcs_uri}")
            return gcs_uri
            
        except Exception as e:
            logger.error(f"Error uploading file to GCS: {e}")
            return None
    
    def download_file(self, gcs_uri: str) -> Optional[str]:
        """
        Download content from GCS.
        
        Args:
            gcs_uri: GCS URI of the file (gs://bucket/path)
            
        Returns:
            Content of the file or None if download fails
        """
        try:
            # Extract bucket and blob name from GCS URI
            if not gcs_uri.startswith("gs://"):
                raise ValueError(f"Invalid GCS URI: {gcs_uri}")
            
            path = gcs_uri[5:]  # Remove "gs://" prefix
            bucket_name, blob_name = path.split("/", 1)
            
            # Download the blob
            bucket = self.storage_client.bucket(bucket_name)
            blob = bucket.blob(blob_name)
            content = blob.download_as_text()
            
            logger.info(f"Successfully downloaded file from {gcs_uri}")
            return content
            
        except Exception as e:
            logger.error(f"Error downloading file from GCS: {e}")
            return None

    def read_file(self, path: str) -> Optional[str]:
        """
        Read a file from GCS.
        
        Args:
            path: Path to the file in the bucket
            
        Returns:
            Content of the file as string or None if read fails
        """
        try:
            blob = self.bucket.blob(path)
            return blob.download_as_text()
        except Exception as e:
            logger.error(f"Error reading file {path}: {str(e)}")
            return None
    
    def write_file(self, path: str, content: str) -> bool:
        """
        Write content to a file in GCS.
        
        Args:
            path: Path where to write the file
            content: Content to write
            
        Returns:
            True if successful, False otherwise
        """
        try:
            blob = self.bucket.blob(path)
            blob.upload_from_string(content)
            return True
        except Exception as e:
            logger.error(f"Error writing file {path}: {str(e)}")
            return False 