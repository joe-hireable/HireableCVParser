import os
import tempfile
import logging
from typing import Tuple, Optional
import requests
from google.cloud import storage
from google.oauth2 import service_account

logger = logging.getLogger(__name__)

class DocumentProcessor:
    """Handles document download and processing operations."""
    
    def __init__(self, key_path: Optional[str] = None):
        """
        Initialize the document processor.
        
        Args:
            key_path: Path to service account JSON key file (optional)
        """
        self.key_path = key_path
        logger.info("Initialized DocumentProcessor")
        
        # Create credentials if key path is provided
        self.credentials = None
        if key_path and os.path.exists(key_path):
            self.credentials = service_account.Credentials.from_service_account_file(key_path)
    
    def download_and_process(self, url: str) -> Optional[str]:
        """
        Download a document from URL or GCS and extract its text content.
        
        Args:
            url: URL or GCS URI of the document to download
            
        Returns:
            Extracted text content or None if processing fails
        """
        try:
            # Check if this is a GCS URI
            if url.startswith('gs://'):
                file_content, content_type = self._download_from_gcs(url)
            else:
                # Regular HTTP URL
                file_content, content_type = self._download_from_url(url)
            
            if not file_content or not content_type:
                logger.warning(f"Failed to download file from {url}")
                return None
            
            # Extract text based on content type
            if "pdf" in content_type.lower():
                return self._extract_text_from_pdf(file_content)
            elif "docx" in content_type.lower() or "document" in content_type.lower():
                return self._extract_text_from_docx(file_content)
            else:
                logger.warning(f"Unsupported content type: {content_type}")
                return None
                
        except Exception as e:
            logger.error(f"Error processing document from {url}: {e}")
            return None
    
    def _download_from_url(self, url: str) -> Tuple[Optional[bytes], Optional[str]]:
        """
        Download a file from a URL.
        
        Args:
            url: URL of the file to download
            
        Returns:
            Tuple of (file_content, content_type) or (None, None) if download fails
        """
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            content_type = response.headers.get('content-type')
            if not content_type:
                # Try to guess content type from URL
                if url.lower().endswith('.pdf'):
                    content_type = 'application/pdf'
                elif url.lower().endswith('.docx'):
                    content_type = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
                else:
                    raise ValueError(f"Unsupported file type: {url}")
            
            logger.info(f"Successfully downloaded file from {url} with content type {content_type}")
            return response.content, content_type
            
        except Exception as e:
            logger.error(f"Error downloading file from {url}: {e}")
            return None, None
    
    def _download_from_gcs(self, gcs_uri: str) -> Tuple[Optional[bytes], Optional[str]]:
        """
        Download a file from Google Cloud Storage.
        
        Args:
            gcs_uri: GCS URI in the format 'gs://bucket-name/path/to/object'
            
        Returns:
            Tuple of (file_content, content_type) or (None, None) if download fails
        """
        try:
            # Parse the GCS URI
            if not gcs_uri.startswith('gs://'):
                logger.error(f"Invalid GCS URI format: {gcs_uri}")
                return None, None
            
            # Remove 'gs://' prefix and split into bucket name and object path
            parts = gcs_uri[5:].split('/', 1)
            if len(parts) != 2:
                logger.error(f"Invalid GCS URI format: {gcs_uri}")
                return None, None
            
            bucket_name, object_name = parts
            
            # Initialize GCS client
            storage_client = storage.Client(credentials=self.credentials)
            bucket = storage_client.bucket(bucket_name)
            blob = bucket.blob(object_name)
            
            # Create a temporary file to store the downloaded content
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_path = temp_file.name
            
            # Download the file
            blob.download_to_filename(temp_path)
            
            # Determine content type
            content_type = blob.content_type
            if not content_type:
                # Try to infer content type from file extension
                if object_name.lower().endswith('.pdf'):
                    content_type = 'application/pdf'
                elif object_name.lower().endswith('.docx'):
                    content_type = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
                else:
                    content_type = 'application/octet-stream'
            
            # Read the file content
            with open(temp_path, 'rb') as f:
                file_content = f.read()
            
            # Clean up the temporary file
            os.unlink(temp_path)
            
            return file_content, content_type
            
        except Exception as e:
            logger.error(f"Error downloading file from {gcs_uri}: {e}")
            return None, None
    
    def _extract_text_from_pdf(self, file_content: bytes) -> Optional[str]:
        """
        Extract text from PDF content.
        
        Args:
            file_content: Binary content of the PDF file
            
        Returns:
            Extracted text or None if extraction fails
        """
        try:
            import io
            import fitz  # PyMuPDF
            
            # Create a file-like object from the binary content
            file_stream = io.BytesIO(file_content)
            
            # Open the PDF with PyMuPDF
            doc = fitz.open(stream=file_stream, filetype="pdf")
            
            # Extract text from all pages
            text = ""
            for page_num in range(len(doc)):
                page = doc[page_num]
                text += page.get_text() + "\n"
            
            # Close the document
            doc.close()
            
            logger.info(f"Successfully extracted {len(text)} characters from PDF")
            return text
            
        except Exception as e:
            logger.error(f"Error extracting text from PDF: {e}")
            return None
    
    def _extract_text_from_docx(self, file_content: bytes) -> Optional[str]:
        """
        Extract text from DOCX content.
        
        Args:
            file_content: Binary content of the DOCX file
            
        Returns:
            Extracted text or None if extraction fails
        """
        try:
            import io
            import docx
            
            # Create a file-like object from the binary content
            file_stream = io.BytesIO(file_content)
            
            # Create a docx document object
            doc = docx.Document(file_stream)
            
            # Extract text from all paragraphs
            text = ""
            for para in doc.paragraphs:
                text += para.text + "\n"
            
            logger.info(f"Successfully extracted {len(text)} characters from DOCX")
            return text
            
        except Exception as e:
            logger.error(f"Error extracting text from DOCX: {e}")
            return None 