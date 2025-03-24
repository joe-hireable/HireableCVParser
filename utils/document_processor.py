import os
import tempfile
import logging
import io
import hashlib
import datetime
from typing import Tuple, Optional

import requests
from google.cloud import storage, firestore
from tenacity import retry, stop_after_attempt, wait_exponential
from opentelemetry import trace
import fitz  # PyMuPDF
import docx

logger = logging.getLogger(__name__)

class DocumentProcessor:
    """Handles document download and processing operations."""
    
    def __init__(self):
        """Initialize the document processor."""
        logger.info("Initialized DocumentProcessor")
        # Initialize storage client with ADC
        self.storage_client = storage.Client()
        # Initialize Firestore client
        self.db = firestore.Client()
        self.tracer = trace.get_tracer(__name__)
        # Cache configuration
        self.cache_ttl_days = 30  # Cache documents for 30 days
        
    def _get_cache_key(self, url: str) -> str:
        """
        Generate a cache key for the given URL.
        
        Args:
            url: URL or GCS URI of the document
            
        Returns:
            MD5 hash of the URL as the cache key
        """
        return hashlib.md5(url.encode()).hexdigest()
        
    def download_and_process(self, url: str) -> Optional[str]:
        """
        Download a document from URL or GCS and extract its text content.
        Implements caching using Firestore.
        
        Args:
            url: URL or GCS URI of the document to download
            
        Returns:
            Extracted text content or None if processing fails
        """
        with self.tracer.start_as_current_span("download_and_process") as span:
            span.set_attribute("url", url)
            try:
                # Generate cache key
                cache_key = self._get_cache_key(url)
                
                # Check cache
                cache_ref = self.db.collection('document_cache').document(cache_key)
                cache_doc = cache_ref.get()
                
                if cache_doc.exists:
                    logger.info(f"Cache hit for {url}")
                    return cache_doc.to_dict().get('content')
                
                # If not in cache, process the document
                if url.startswith('gs://'):
                    file_content, content_type = self._download_from_gcs(url)
                else:
                    file_content, content_type = self._download_from_url(url)
                
                if not file_content or not content_type:
                    logger.warning(f"Failed to download file from {url}")
                    return None
                
                # Extract text based on content type
                text_content = None
                if "pdf" in content_type.lower():
                    text_content = self._extract_text_from_pdf(file_content)
                elif "docx" in content_type.lower() or "document" in content_type.lower():
                    text_content = self._extract_text_from_docx(file_content)
                else:
                    logger.warning(f"Unsupported content type: {content_type}")
                    return None
                
                # Cache the result if successful
                if text_content:
                    cache_ref.set({
                        'content': text_content,
                        'url': url,
                        'content_type': content_type,
                        'timestamp': firestore.SERVER_TIMESTAMP,
                        'expiration': firestore.SERVER_TIMESTAMP + datetime.timedelta(days=self.cache_ttl_days)
                    })
                    logger.info(f"Cached document content for {url}")
                    span.set_status(trace.Status(trace.StatusCode.OK))
                else:
                    span.set_status(trace.Status(trace.StatusCode.ERROR, "Failed to process document"))
                return text_content
                
            except Exception as e:
                span.set_status(trace.Status(trace.StatusCode.ERROR, str(e)))
                logger.error(f"Error processing document from {url}: {e}")
                return None
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def _download_from_url(self, url: str) -> Tuple[Optional[bytes], Optional[str]]:
        """
        Download a file from a URL with retry logic.
        
        Args:
            url: URL of the file to download
            
        Returns:
            Tuple of (file_content, content_type) or (None, None) if download fails
        """
        try:
            response = requests.get(url)
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
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def _download_from_gcs(self, gcs_uri: str) -> Tuple[Optional[bytes], Optional[str]]:
        """
        Download a file from Google Cloud Storage with retry logic.
        
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
            
            # Get bucket and blob
            bucket = self.storage_client.bucket(bucket_name)
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