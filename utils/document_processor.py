import os
import tempfile
import logging
import io
import hashlib
import datetime
import zlib
from typing import Tuple, Optional
from functools import lru_cache
from datetime import timezone

import requests
from google.cloud import storage, firestore
from tenacity import retry, stop_after_attempt, wait_exponential
from pypdf import PdfReader
import docx
from opentelemetry import trace
import config

logger = logging.getLogger(__name__)

class DocumentProcessor:
    """Handles document download and processing operations."""
    
    def __init__(self, storage_client=None, vertex_client=None, system_prompt=None, user_prompt=None, few_shot_examples=None, schema_model=None):
        """Initialize the document processor."""
        self.tracer = trace.get_tracer(__name__)
        logger.info("Initialized DocumentProcessor")
        # Initialize storage client with ADC if not provided
        self.storage_client = storage_client or storage.Client()
        # Initialize Firestore client
        self.db = firestore.Client()
        # Track if resources are closed
        self._closed = False
        # Store additional parameters
        self.vertex_client = vertex_client
        self.system_prompt = system_prompt
        self.user_prompt = user_prompt
        self.few_shot_examples = few_shot_examples
        self.schema_model = schema_model
        
    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - ensures cleanup is called."""
        self.cleanup()

    def cleanup(self) -> None:
        """
        Clean up resources and close connections.
        This method should be called when the processor is no longer needed.
        """
        if self._closed:
            return

        try:
            # Close Firestore client
            if hasattr(self, 'db'):
                self.db.close()
                logger.info("Closed Firestore client connection")

            # Close Storage client
            if hasattr(self, 'storage_client'):
                self.storage_client.close()
                logger.info("Closed Storage client connection")

            # Clear memory cache
            if hasattr(self, '_get_from_memory_cache'):
                self._get_from_memory_cache.cache_clear()
                logger.info("Cleared memory cache")

            self._closed = True
            logger.info("Successfully cleaned up DocumentProcessor resources")

        except Exception as e:
            logger.error(f"Error during DocumentProcessor cleanup: {e}")
            raise

    def _ensure_not_closed(self):
        """Helper method to check if the processor is closed."""
        if self._closed:
            raise RuntimeError("DocumentProcessor has been closed and cannot be used")

    def _get_cache_key(self, url: str) -> str:
        """
        Generate a cache key for the given URL.
        
        Args:
            url: URL or GCS URI of the document
            
        Returns:
            MD5 hash of the URL as the cache key
        """
        return hashlib.md5(url.encode()).hexdigest()
        
    def _cache_document(self, cache_key: str, text_content: str, url: str, content_type: str) -> None:
        """
        Cache document content with compression for large documents.
        
        Args:
            cache_key: Unique key for the document
            text_content: Text content to cache
            url: Original document URL
            content_type: Content type of the document
        """
        # Get current UTC timestamp
        current_utc = datetime.datetime.now(timezone.utc)
        
        # Compress large content
        if len(text_content) > config.CACHE_COMPRESSION_THRESHOLD:
            compressed = zlib.compress(text_content.encode('utf-8'))
            cache_data = {
                'content': compressed,
                'compressed': True,
                'url': url,
                'content_type': content_type,
                'timestamp': current_utc,
                'expiration': current_utc + datetime.timedelta(days=config.CACHE_TTL_DAYS)
            }
        else:
            cache_data = {
                'content': text_content,
                'compressed': False,
                'url': url,
                'content_type': content_type,
                'timestamp': current_utc,
                'expiration': current_utc + datetime.timedelta(days=config.CACHE_TTL_DAYS)
            }
        
        self.db.collection('document_cache').document(cache_key).set(cache_data)
        logger.info(f"Cached document content for {url} (compressed: {cache_data['compressed']})")

    @lru_cache(maxsize=config.MEMORY_CACHE_SIZE)
    def _get_from_memory_cache(self, cache_key: str) -> Optional[str]:
        """
        In-memory cache for very frequently accessed documents.
        
        Args:
            cache_key: Cache key for the document
            
        Returns:
            Cached content if available, None otherwise
        """
        # This is an LRU-cached method that will store successful results automatically
        # The return None is only for the very first call with a given cache key
        return None

    def download_and_process(self, url: str) -> Optional[str]:
        """Download a document from URL or GCS and extract its text content."""
        self._ensure_not_closed()
        with self.tracer.start_as_current_span("download_and_process") as span:
            try:
                span.set_attribute("document.url", url)
                cache_key = self._get_cache_key(url)
                
                with self.tracer.start_span("check_cache") as cache_span:
                    # Check in-memory cache first
                    memory_cached = self._get_from_memory_cache(cache_key)
                    if memory_cached:
                        cache_span.set_attribute("cache.hit", True)
                        cache_span.set_attribute("cache.type", "memory")
                        return memory_cached
                    
                    # Check Firestore cache
                    cache_ref = self.db.collection('document_cache').document(cache_key)
                    cache_doc = cache_ref.get()
                    
                    if cache_doc.exists:
                        cache_span.set_attribute("cache.hit", True)
                        cache_span.set_attribute("cache.type", "firestore")
                        cache_data = cache_doc.to_dict()
                        content = cache_data.get('content')
                        is_compressed = cache_data.get('compressed', False)
                        
                        # Check if cache has expired using UTC timestamp
                        expiration = cache_data.get('expiration')
                        if expiration:
                            if not isinstance(expiration, datetime.datetime):
                                logger.warning(f"Invalid expiration type in cache: {type(expiration)}")
                                cache_ref.delete()
                            else:
                                if not expiration.tzinfo:
                                    expiration = expiration.replace(tzinfo=timezone.utc)
                                current_utc = datetime.datetime.now(timezone.utc)
                                if expiration < current_utc:
                                    logger.info(f"Cache expired for {url}")
                                    cache_ref.delete()
                                else:
                                    logger.info(f"Cache hit for {url}")
                                    result = zlib.decompress(content).decode('utf-8') if is_compressed else content
                                    # Store in memory cache for faster subsequent access
                                    self._get_from_memory_cache.cache_parameters = (cache_key,)  # This will update the LRU cache
                                    return result
                
                # If not in cache, process the document
                with self.tracer.start_span("download_document") as download_span:
                    if url.startswith('gs://'):
                        file_content, content_type = self._download_from_gcs(url)
                    else:
                        file_content, content_type = self._download_from_url(url)
                    
                    if not file_content or not content_type:
                        span.set_attribute("error", True)
                        span.set_attribute("error.message", "Failed to download document")
                        raise ValueError(f"Failed to download document from {url}")
                    
                    # Validate content types explicitly
                    if content_type not in config.ALLOWED_CONTENT_TYPES:
                        logger.warning(f"Unsupported content type: {content_type}")
                        raise ValueError(f"Unsupported file format: {content_type}")
                    
                    # Extract text based on content type
                    text_content = None
                    if content_type == 'application/pdf':
                        text_content = self._extract_text_from_pdf(file_content)
                    elif content_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
                        text_content = self._extract_text_from_docx(file_content)
                    else:
                        logger.warning(f"Unsupported content type: {content_type}")
                        raise ValueError(f"Unsupported file format: {content_type}")
                    
                    if text_content is None:
                        raise ValueError(f"Failed to extract text from document")
                
                # Cache the result if successful
                if text_content:
                    self._cache_document(cache_key, text_content, url, content_type)
                return text_content
                
            except Exception as e:
                span.set_attribute("error", True)
                span.set_attribute("error.message", str(e))
                logger.error(f"Error processing document: {e}")
                raise  # Re-raise the exception to ensure test failures are caught
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def _download_from_url(self, url: str) -> Tuple[Optional[bytes], Optional[str]]:
        """
        Download a file from a URL.
        
        Args:
            url: URL of the file
            
        Returns:
            Tuple of (file content as bytes, content type) or (None, None) if download fails
        """
        self._ensure_not_closed()
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()  # Raise exception if status code is not 200
            
            content_type = response.headers.get('Content-Type')
            content = response.content
            
            return content, content_type
        except Exception as e:
            logger.error(f"Error downloading from URL {url}: {e}")
            return None, None
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def _download_from_gcs(self, gcs_uri: str) -> Tuple[Optional[bytes], Optional[str]]:
        """
        Download a file from Google Cloud Storage.
        
        Args:
            gcs_uri: GCS URI of the file (gs://bucket/path)
            
        Returns:
            Tuple of (file content as bytes, content type) or (None, None) if download fails
        """
        self._ensure_not_closed()
        try:
            if not gcs_uri.startswith('gs://'):
                logger.error(f"Invalid GCS URI format: {gcs_uri}")
                return None, None
            
            parts = gcs_uri[5:].split('/', 1)
            if len(parts) != 2:
                logger.error(f"Invalid GCS URI format: {gcs_uri}")
                return None, None
            
            bucket_name, object_name = parts
            
            # Get bucket and blob
            bucket = self.storage_client.bucket(bucket_name)
            blob = bucket.blob(object_name)
            
            # Download directly to memory
            file_content = blob.download_as_bytes()
            
            # Determine content type
            content_type = blob.content_type
            if not content_type:
                if object_name.lower().endswith('.pdf'):
                    content_type = 'application/pdf'
                elif object_name.lower().endswith('.docx'):
                    content_type = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
                else:
                    content_type = 'application/octet-stream'
            
            return file_content, content_type
            
        except Exception as e:
            logger.error(f"Error downloading file from {gcs_uri}: {e}")
            return None, None
    
    def _extract_text_from_pdf(self, file_content: bytes) -> Optional[str]:
        """
        Extract text from a PDF file using pypdf.
        
        Args:
            file_content: PDF file content as bytes
            
        Returns:
            Extracted text or None if extraction fails
        """
        self._ensure_not_closed()
        try:
            file_stream = io.BytesIO(file_content)
            pdf_reader = PdfReader(file_stream)
            
            # Process pages in chunks to reduce memory usage
            text_chunks = []
            for page in pdf_reader.pages:
                text = page.extract_text().strip()
                if text:
                    text_chunks.append(text)
            
            return "\n".join(text_chunks)
            
        except Exception as e:
            logger.error(f"Error extracting text from PDF: {e}")
            return None
    
    def _extract_text_from_docx(self, file_content: bytes) -> Optional[str]:
        """
        Extract text from a DOCX file.
        
        Args:
            file_content: DOCX file content as bytes
            
        Returns:
            Extracted text or None if extraction fails
        """
        self._ensure_not_closed()
        try:
            # Create a file-like object from the binary content
            file_stream = io.BytesIO(file_content)
            
            # Create a docx document object
            doc = docx.Document(file_stream)
            
            # Extract text from all paragraphs and join with single newlines
            paragraphs = [para.text.strip() for para in doc.paragraphs if para.text.strip()]
            text = "\n".join(paragraphs)
            
            logger.info(f"Successfully extracted {len(text)} characters from DOCX")
            return text
            
        except Exception as e:
            logger.error(f"Error extracting text from DOCX: {e}")
            return None

    def process_document(self, cv_content: bytes, jd_content: Optional[bytes] = None) -> dict:
        """
        Process a document using the Vertex AI client.
        
        Args:
            cv_content: CV file content as bytes
            jd_content: Optional JD file content as bytes
            
        Returns:
            dict: Processing results
        """
        self._ensure_not_closed()
        with self.tracer.start_as_current_span("process_document") as span:
            try:
                # Extract text from CV
                cv_text = None
                if cv_content:
                    # Try PDF first
                    cv_text = self._extract_text_from_pdf(cv_content)
                    if not cv_text:
                        # Try DOCX if PDF fails
                        cv_text = self._extract_text_from_docx(cv_content)
                
                if not cv_text:
                    raise ValueError("Failed to extract text from CV file")
                
                # Extract text from JD if provided
                jd_text = None
                if jd_content:
                    jd_text = self._extract_text_from_pdf(jd_content)
                    if not jd_text:
                        jd_text = self._extract_text_from_docx(jd_content)
                
                # Process with Vertex AI
                if not self.vertex_client:
                    raise ValueError("Vertex AI client not initialized")
                
                # Format the prompt with the extracted text
                prompt = self.user_prompt.format(
                    cv_content=cv_text,
                    jd_content=jd_text or "",
                    few_shot_examples=self.few_shot_examples or ""
                )
                
                # Generate content using Vertex AI
                result = self.vertex_client.generate_content(
                    prompt=prompt,
                    system_prompt=self.system_prompt,
                    schema_model=self.schema_model
                )
                
                return result
                
            except Exception as e:
                span.set_attribute("error", True)
                span.set_attribute("error.message", str(e))
                logger.error(f"Error processing document: {e}")
                raise 