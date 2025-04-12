import logging
from google.cloud import storage
from typing import Optional
import os

logger = logging.getLogger(__name__)

class StorageClient:
    """Client for interacting with Google Cloud Storage."""
    
    def __init__(self, bucket_name: str):
        """
        Initialize the Storage client.
        
        Args:
            bucket_name: Name of the GCS bucket to use
            
        Raises:
            Exception: If client initialization fails
        """
        self.bucket_name = bucket_name
        
        try:
            # Initialize client with ADC
            self.storage_client = storage.Client()
            self.bucket = self.storage_client.bucket(bucket_name)
            logger.info(f"Initialized Storage client for bucket {bucket_name} using ADC")
            
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

    def save_bytes_to_gcs(self, file_bytes: bytes, gcs_path: str, content_type: Optional[str] = None) -> Optional[str]:
        """
        Upload raw file bytes to GCS.

        Args:
            file_bytes: The bytes of the file to upload.
            gcs_path: The full path within the GCS bucket (e.g., 'uploads/user123/cv.pdf').
            content_type: The MIME type of the file (e.g., 'application/pdf').

        Returns:
            The gs:// URI of the uploaded file, or None if upload fails.
        """
        try:
            blob = self.bucket.blob(gcs_path)
            blob.upload_from_string(file_bytes, content_type=content_type)
            gcs_uri = f"gs://{self.bucket_name}/{gcs_path}"
            logger.info(f"Successfully uploaded bytes to {gcs_uri}")
            return gcs_uri
        except Exception as e:
            logger.error(f"Error uploading bytes to GCS path {gcs_path}: {e}")
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