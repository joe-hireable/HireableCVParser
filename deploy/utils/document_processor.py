import os
import tempfile
import logging
from typing import Tuple, Optional
import requests
from google.cloud import storage

logger = logging.getLogger(__name__)

class DocumentProcessor:
    """Handles document download and processing operations."""
    
    def __init__(self):
        """Initialize the document processor."""
        logger.info("Initialized DocumentProcessor")
    
    def download_and_process(self, url: str) -> Optional[str]:
        """
        Download a document from URL and extract its text content.
        
        Args:
            url: URL of the document to download
            
        Returns:
            Extracted text content or None if processing fails
        """
        try:
            # Download file content
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
            from pypdf import PdfReader
            
            # Create a file-like object from the binary content
            file_stream = io.BytesIO(file_content)
            
            # Create a PDF reader object
            reader = PdfReader(file_stream)
            
            # Extract text from all pages
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            
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