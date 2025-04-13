import pytest
from unittest.mock import patch, MagicMock, ANY
from utils.document_processor import DocumentProcessor
import io
import datetime
from datetime import timezone
from contextlib import contextmanager


class MockSpan:
    def __init__(self):
        self.attributes = {}

    def set_attribute(self, key, value):
        self.attributes[key] = value

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class MockTracer:
    def __init__(self):
        self.current_span = MockSpan()

    def start_as_current_span(self, name):
        return self.current_span

    def start_span(self, name):
        return self.current_span


class TestDocumentProcessor:
    """Test cases for DocumentProcessor."""

    @pytest.fixture
    def document_processor(self):
        """Create a DocumentProcessor instance for testing."""
        with patch('utils.document_processor.storage.Client'), \
             patch('utils.document_processor.firestore.Client'), \
             patch('utils.document_processor.trace.get_tracer') as mock_get_tracer:
            mock_get_tracer.return_value = MockTracer()
            processor = DocumentProcessor()
            # Ensure db is initialized
            processor.db = MagicMock()
            return processor

    @patch("utils.document_processor.PdfReader")
    def test_extract_text_from_pdf(self, mock_pdf_reader, document_processor):
        """Test extracting text from a PDF file."""
        # Mock the PDF document and page
        mock_page = MagicMock()
        mock_page.extract_text.return_value = "Sample PDF text content"
        mock_pdf_reader.return_value.pages = [mock_page]

        # Test with a mock file content
        pdf_content = b"dummy PDF content"
        result = document_processor._extract_text_from_pdf(pdf_content)

        # Verify PdfReader was called with the correct arguments
        mock_pdf_reader.assert_called_once()
        # Check that the first argument is a BytesIO object
        assert isinstance(mock_pdf_reader.call_args[0][0], io.BytesIO)

        # Check returned text
        assert result == "Sample PDF text content"

    @patch("utils.document_processor.docx.Document")
    def test_extract_text_from_docx(self, mock_docx_document, document_processor):
        """Test extracting text from a DOCX file."""
        # Mock the DOCX document and paragraphs
        mock_doc = MagicMock()
        mock_para1 = MagicMock()
        mock_para1.text = "First paragraph"
        mock_para2 = MagicMock()
        mock_para2.text = "Second paragraph"
        mock_doc.paragraphs = [mock_para1, mock_para2]
        mock_docx_document.return_value = mock_doc

        # Test with a mock file content
        docx_content = b"dummy DOCX content"
        result = document_processor._extract_text_from_docx(docx_content)

        # Verify docx.Document was called with the correct arguments
        mock_docx_document.assert_called_once()
        # Check that the first argument is a BytesIO object
        assert isinstance(mock_docx_document.call_args[0][0], io.BytesIO)

        # Check returned text - should have newlines between paragraphs
        assert result == "First paragraph\nSecond paragraph"

    @patch("utils.document_processor.PdfReader", side_effect=Exception("PDF error"))
    def test_extract_text_from_pdf_error(self, mock_pdf_reader, document_processor):
        """Test handling errors when extracting text from a PDF file."""
        # Test with a mock file content
        pdf_content = b"corrupt PDF content"
        result = document_processor._extract_text_from_pdf(pdf_content)

        # Verify PdfReader was called
        mock_pdf_reader.assert_called_once()

        # Check that None is returned on error
        assert result is None

    @patch("utils.document_processor.docx.Document", side_effect=Exception("DOCX error"))
    def test_extract_text_from_docx_error(self, mock_docx_document, document_processor):
        """Test handling errors when extracting text from a DOCX file."""
        # Test with a mock file content
        docx_content = b"corrupt DOCX content"
        result = document_processor._extract_text_from_docx(docx_content)

        # Verify docx.Document was called
        mock_docx_document.assert_called_once()

        # Check that None is returned on error
        assert result is None

    @patch("utils.document_processor.DocumentProcessor._download_from_url")
    @patch("utils.document_processor.DocumentProcessor._extract_text_from_pdf")
    @patch("utils.document_processor.DocumentProcessor._get_from_memory_cache")
    def test_download_and_process_pdf(self, mock_memory_cache, mock_extract_pdf, mock_download, document_processor):
        """Test downloading and processing a PDF file."""
        # Setup mocks
        mock_download.return_value = (b"PDF content", "application/pdf")
        mock_extract_pdf.return_value = "Extracted PDF text"
        mock_memory_cache.return_value = None

        # Mock cache document
        mock_cache_doc = MagicMock()
        mock_cache_doc.exists = False
        document_processor.db.collection.return_value.document.return_value = mock_cache_doc

        # Test with a URL
        test_url = "https://example.com/test.pdf"
        result = document_processor.download_and_process(test_url)

        # Verify mocks were called
        mock_download.assert_called_once_with(test_url)
        mock_extract_pdf.assert_called_once_with(b"PDF content")

        # Check result
        assert result == "Extracted PDF text"

    @patch("utils.document_processor.DocumentProcessor._download_from_gcs")
    @patch("utils.document_processor.DocumentProcessor._extract_text_from_docx")
    @patch("utils.document_processor.DocumentProcessor._get_from_memory_cache")
    def test_download_and_process_docx(self, mock_memory_cache, mock_extract_docx, mock_download, document_processor):
        """Test downloading and processing a DOCX file."""
        # Setup mocks
        mock_download.return_value = (b"DOCX content", "application/vnd.openxmlformats-officedocument.wordprocessingml.document")
        mock_extract_docx.return_value = "Extracted DOCX text"
        mock_memory_cache.return_value = None

        # Mock cache document
        mock_cache_doc = MagicMock()
        mock_cache_doc.exists = False
        document_processor.db.collection.return_value.document.return_value = mock_cache_doc

        # Test with a GCS URI
        test_gcs_uri = "gs://bucket/test.docx"
        result = document_processor.download_and_process(test_gcs_uri)

        # Verify mocks were called
        mock_download.assert_called_once_with(test_gcs_uri)
        mock_extract_docx.assert_called_once_with(b"DOCX content")

        # Check result
        assert result == "Extracted DOCX text"

    @patch("utils.document_processor.DocumentProcessor._download_from_url")
    @patch("utils.document_processor.DocumentProcessor._download_from_gcs")
    @patch("utils.document_processor.DocumentProcessor._get_from_memory_cache")
    def test_download_and_process_unsupported_format(self, mock_memory_cache, mock_download_gcs, mock_download_url, document_processor):
        """Test handling unsupported file formats."""
        # Setup mocks
        mock_download_url.return_value = (b"unknown content", "application/octet-stream")
        mock_download_gcs.return_value = (b"unknown content", "application/octet-stream")
        mock_memory_cache.return_value = None

        # Mock cache document
        mock_cache_doc = MagicMock()
        mock_cache_doc.exists = False
        document_processor.db.collection.return_value.document.return_value = mock_cache_doc

        # Test with an unsupported file extension
        with pytest.raises(ValueError, match="Unsupported file format"):
            document_processor.download_and_process("https://example.com/test.unknown")

        # Test with an unsupported content type
        with pytest.raises(ValueError, match="Unsupported file format"):
            document_processor.download_and_process("gs://bucket/test.unknown") 