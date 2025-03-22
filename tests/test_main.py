"""Tests for CV Optimizer Cloud Function."""

import json
import unittest
from unittest.mock import patch, MagicMock

import src.main as main
from utils.gemini_client import GeminiClient
from utils.storage import StorageClient
from utils.document_processor import DocumentProcessor

class TestCVOptimizer(unittest.TestCase):
    """Tests for CV Optimizer Cloud Function."""
    
    @patch('src.main.StorageClient')
    @patch('src.main.DocumentProcessor')
    @patch('src.main.GeminiClient')
    @patch('src.main.fetch_resources')
    def test_cv_optimizer_success(self, mock_fetch_resources, mock_gemini_client,
                                 mock_doc_processor, mock_storage_client):
        """Test successful execution of the CV optimizer function."""
        # Mock request
        mock_request = MagicMock()
        mock_request.method = 'POST'
        mock_request.get_json.return_value = {
            'cv_url': 'https://example.com/cv.pdf',
            'jd_url': 'https://example.com/jd.pdf',
            'task': 'parsing',
            'section': 'summary'
        }
        
        # Mock client instances
        mock_storage_instance = MagicMock()
        mock_storage_client.return_value = mock_storage_instance
        
        mock_doc_instance = MagicMock()
        mock_doc_instance.download_and_process.side_effect = ["CV content", "JD content"]
        mock_doc_processor.return_value = mock_doc_instance
        
        mock_gemini_instance = MagicMock()
        mock_gemini_instance.generate_text.return_value = {
            "status": "success",
            "data": {
                "firstName": "John",
                "surname": "Doe"
            },
            "errors": []
        }
        mock_gemini_client.return_value = mock_gemini_instance
        
        # Mock resource fetching
        mock_fetch_resources.return_value = (
            "System prompt",
            "User prompt with {section}, {cv_content}, {jd_content}, {few_shot_examples}",
            "Few shot examples",
            {"type": "object"}
        )
        
        # Call function
        response = main.cv_optimizer(mock_request)
        
        # Assert response
        self.assertEqual(response[1], 200)  # HTTP status code
        self.assertEqual(json.loads(response[0]), {"firstName": "John", "surname": "Doe"})
        
        # Verify method calls
        mock_doc_instance.download_and_process.assert_any_call('https://example.com/cv.pdf')
        mock_doc_instance.download_and_process.assert_any_call('https://example.com/jd.pdf')
        mock_fetch_resources.assert_called_once_with('parsing')
        mock_gemini_instance.generate_text.assert_called_once()

    @patch('src.main.load_resource_file')
    def test_fetch_resources(self, mock_load_resource_file):
        """Test fetching resources based on task."""
        # Mock resource loading
        mock_load_resource_file.side_effect = [
            "System prompt content",
            "User prompt content",
            "Few shot examples content",
            '{"type": "object", "properties": {"firstName": {"type": "string"}}}'
        ]
        
        # Call function
        system_prompt, user_prompt, few_shot_examples, schema = main.fetch_resources('parsing')
        
        # Assert results
        self.assertEqual(system_prompt, "System prompt content")
        self.assertEqual(user_prompt, "User prompt content")
        self.assertEqual(few_shot_examples, "Few shot examples content")
        self.assertEqual(schema, {"type": "object", "properties": {"firstName": {"type": "string"}}})
        
        # Verify method calls
        mock_load_resource_file.assert_any_call('parsing', 'system_prompt')
        mock_load_resource_file.assert_any_call('parsing', 'user_prompt')
        mock_load_resource_file.assert_any_call('parsing', 'examples')
        mock_load_resource_file.assert_any_call('parsing', 'schema')

if __name__ == '__main__':
    unittest.main() 