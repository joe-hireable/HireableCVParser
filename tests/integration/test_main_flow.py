import json
import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path
import functions_framework
from werkzeug.datastructures import FileStorage, Headers
import io
from flask import Request
from werkzeug.test import EnvironBuilder
import google.cloud.aiplatform as aiplatform
from vertexai.generative_models import GenerativeModel as VertexGenerativeModel

# Import main application module (assuming it's structured like this)
import main
from models.schemas import ParsingResponseSchema, ScoringResponseSchema
from models.schemas import ParsingDataModel, SkillModel, SkillProficiencyEnum, SkillTypeEnum, ExperienceModel, EducationModel, LocationModel
from models.schemas import ScoresModel, FeedbackModel, ScoringDataModel

# Mock resource loading function
def mock_load_resource_file(task, resource_type):
    if resource_type == 'system_prompt':
        return "Mock system prompt"
    elif resource_type == 'user_prompt':
        return f"Mock user prompt for {task} with {{cv_content}}, {{jd_content}}, {{few_shot_examples}}"
    elif resource_type == 'schema':
        # Return a minimal valid JSON schema string representation if needed,
        # but fetch_resources primarily needs the model class now.
        # We rely on SCHEMA_REGISTRY providing the model directly.
        # For simplicity, we assume the real SCHEMA_REGISTRY works.
        return "{}" # Minimal JSON, not strictly needed if model is primary
    elif resource_type == 'examples':
        return "Mock few shot examples"
    return None

class TestMainFlow:
    """Integration tests for the main application flow."""
    
    @pytest.fixture(autouse=True)
    def setup_app_context(self):
        """Setup Flask application context for all tests."""
        with main.app.app_context():
            yield
    
    def _build_request(self, data, files=None, headers=None, method='POST'):
        """Helper function to build a Flask Request object."""
        # Convert files to the format expected by EnvironBuilder
        if files:
            # Create a multipart form data
            builder = EnvironBuilder(
                method=method,
                data=data,
                headers=Headers(headers) if headers else None
            )
            # Add files to the builder's files dictionary
            for key, file in files.items():
                builder.files[key] = file
        else:
            builder = EnvironBuilder(
                method=method,
                data=data,
                headers=Headers(headers) if headers else None
            )
        
        environ = builder.get_environ()
        return Request(environ)

    @patch("main.load_resource_file", side_effect=mock_load_resource_file)
    @patch("main.verify_supabase_jwt")
    @patch("main.DocumentProcessor")
    @patch("main.StorageClient")
    @patch("google.cloud.aiplatform.init")
    @patch("vertexai.generative_models.GenerativeModel")
    @patch("utils.gemini_client.GeminiClient.generate_content")
    def test_parsing_request(self, mock_generate_content, mock_vertex_model, mock_aiplatform_init, 
                           mock_storage_client_class, mock_doc_processor_class, 
                           mock_verify_jwt, mock_loader, sample_cv_path):
        """Test the parsing task flow through the API with Vertex AI."""
        # Configure mocks
        mock_verify_jwt.return_value = {'sub': 'mock-user-id'}
        
        # Mock Storage Client
        mock_storage = MagicMock()
        mock_storage.save_bytes_to_gcs.return_value = "gs://mock-bucket/mock_cv.pdf"
        mock_storage_client_class.return_value = mock_storage
        
        # Mock document processor
        mock_doc_processor = MagicMock()
        mock_doc_processor.download_and_process.return_value = "Extracted CV text"
        mock_doc_processor_class.return_value = mock_doc_processor
        
        # Mock Gemini client directly - this bypasses the Vertex AI call
        mock_parsing_data = {
            "firstName": "John",
            "surname": "Doe",
            "email": "john.doe@example.com",
            "phone": "+44 7700 900000",
            "headline": "Senior Software Engineer",
            "profileStatement": "Software Engineer profile",
            "skills": [
                {
                    "name": "Python",
                    "proficiency": "Advanced",
                    "skillType": "hard"
                },
                {
                    "name": "JavaScript",
                    "proficiency": "Intermediate",
                    "skillType": "hard"
                },
                {
                    "name": "GCP",
                    "proficiency": "Intermediate",
                    "skillType": "hard"
                }
            ],
            "achievements": ["Achievement 1", "Achievement 2"],
            "experience": [
                {
                    "company": "Tech Innovations Ltd",
                    "title": "Senior Software Engineer",
                    "start": "January 2021",
                    "current": True,
                    "summary": "Working on cloud solutions",
                    "highlights": ["Task 1", "Task 2"]
                }
            ],
            "education": [
                {
                    "institution": "University of London",
                    "qualification": "BSc",
                    "course": "Computer Science",
                    "start": "September 2012",
                    "end": "June 2016",
                    "grade": "2:1",
                    "location": {
                        "city": "London",
                        "country": "United Kingdom"
                    }
                }
            ]
        }

        # Set up the mock successful response from the Gemini client
        mock_generate_content.return_value = {
            "status": "success",
            "data": mock_parsing_data
        }
        
        # Create test CV file for upload
        with open(sample_cv_path, 'rb') as f:
            cv_file_content = f.read()
        
        # Create a FileStorage object for the test file
        cv_file = FileStorage(
            stream=io.BytesIO(cv_file_content),
            filename=sample_cv_path.name,
            content_type='application/pdf'
        )
        
        # Build the request
        request_data = {'task': 'parsing'}
        request_files = {'cv_file': cv_file}
        request_headers = {
            'Authorization': 'Bearer mock-token',
            'Content-Type': 'multipart/form-data; boundary=---testboundary'
        }
        
        request = self._build_request(request_data, files=request_files, headers=request_headers)

        # Call the function
        response = main.cv_optimizer(request)
        
        # Assertions
        assert response.status_code == 200
        response_data = json.loads(response.data)
        
        # Verify the response structure - this should match the structure from mock_parsing_data
        assert response_data['firstName'] == "John"
        assert response_data['surname'] == "Doe"
        assert response_data['email'] == "john.doe@example.com"
        
        # Verify our mocks were called correctly
        mock_verify_jwt.assert_called_once()
        mock_doc_processor_class.assert_called_once()
        mock_doc_processor.download_and_process.assert_called_once()
        mock_aiplatform_init.assert_called_once()
        mock_generate_content.assert_called_once()
    
    @patch("main.load_resource_file", side_effect=mock_load_resource_file)
    @patch("main.verify_supabase_jwt")
    @patch("main.DocumentProcessor")
    @patch("main.StorageClient")
    @patch("google.cloud.aiplatform.init")
    @patch("vertexai.generative_models.GenerativeModel")
    @patch("utils.gemini_client.GeminiClient.generate_content")
    def test_scoring_request(self, mock_generate_content, mock_vertex_model, mock_aiplatform_init,
                           mock_storage_client_class, mock_doc_processor_class,
                           mock_verify_jwt, mock_loader,
                           sample_cv_path, sample_jd_path):
        """Test the scoring task flow through the API with Vertex AI."""
        # Configure mocks
        mock_verify_jwt.return_value = {'sub': 'mock-user-id'}
        
        # Mock Storage Client
        mock_storage = MagicMock()
        mock_storage.save_bytes_to_gcs.return_value = "gs://mock-bucket/mock_cv.pdf"
        mock_storage.save_webpage_as_pdf.return_value = "gs://mock-bucket/mock_jd.pdf"
        mock_storage_client_class.return_value = mock_storage
        
        # Mock document processor
        mock_doc_processor = MagicMock()
        mock_doc_processor.download_and_process.side_effect = ["Extracted CV text", "Extracted JD text"]
        mock_doc_processor_class.return_value = mock_doc_processor
        
        # Create direct mock data
        mock_scoring_data = {
            "scores": {
                "overall": 85,
                "relevance": 83,
                "skillsAlignment": 90,
                "experienceMatch": 80,
                "achievementFocus": 82,
                "presentation": 86,
                "atsCompatibility": 89
            },
            "feedback": {
                "strengths": ["Strong Python skills", "Relevant cloud experience"],
                "areasToImprove": ["Limited team leadership", "Missing project management experience"]
            },
            "matchAssessment": "Good overall fit for the role with strong technical skills but could improve leadership experience."
        }

        # Set up the mock successful response from the Gemini client
        mock_generate_content.return_value = {
            "status": "success",
            "data": mock_scoring_data
        }
        
        # Create test files
        with open(sample_cv_path, 'rb') as f:
            cv_file_content = f.read()
        with open(sample_jd_path, 'rb') as f:
            jd_file_content = f.read()
        
        # Create FileStorage objects
        cv_file = FileStorage(
            stream=io.BytesIO(cv_file_content),
            filename=sample_cv_path.name,
            content_type='application/pdf'
        )
        jd_file = FileStorage(
            stream=io.BytesIO(jd_file_content),
            filename=sample_jd_path.name,
            content_type='application/pdf'
        )
        
        # Build the request
        request_data = {'task': 'scoring'}
        request_files = {
            'cv_file': cv_file,
            'jd_file': jd_file
        }
        request_headers = {
            'Authorization': 'Bearer mock-token',
            'Content-Type': 'multipart/form-data; boundary=---testboundary'
        }
        
        request = self._build_request(request_data, files=request_files, headers=request_headers)

        # Call the function
        response = main.cv_optimizer(request)
        
        # Assertions
        assert response.status_code == 200
        response_data = json.loads(response.data)
        
        # Verify the response structure - this should match the structure from mock_scoring_data
        assert 'scores' in response_data
        assert response_data['scores']['overall'] == 85
        assert response_data['scores']['relevance'] == 83
        assert 'feedback' in response_data
        assert 'strengths' in response_data['feedback']
        assert 'areasToImprove' in response_data['feedback']
        assert response_data['matchAssessment'] == "Good overall fit for the role with strong technical skills but could improve leadership experience."
        
        # Verify our mocks were called correctly
        mock_verify_jwt.assert_called_once()
        mock_doc_processor_class.assert_called_once()
        assert mock_doc_processor.download_and_process.call_count >= 1
        mock_aiplatform_init.assert_called_once()
        mock_generate_content.assert_called_once()

    @patch("main.load_resource_file", side_effect=mock_load_resource_file)
    @patch("main.verify_supabase_jwt")
    @patch("main.DocumentProcessor")
    @patch("main.StorageClient")
    @patch("google.cloud.aiplatform.init")
    @patch("vertexai.generative_models.GenerativeModel")
    @patch("utils.gemini_client.GeminiClient.generate_content")
    def test_error_handling(self, mock_generate_content, mock_vertex_model, mock_aiplatform_init,
                          mock_storage_client_class, mock_doc_processor_class,
                          mock_verify_jwt, mock_loader, sample_cv_path):
        """Test error handling in the API with Vertex AI."""
        # Configure mocks
        mock_verify_jwt.return_value = {'sub': 'mock-user-id'}
        
        # Mock Storage Client
        mock_storage = MagicMock()
        mock_storage.save_bytes_to_gcs.return_value = "gs://mock-bucket/mock_cv.pdf"
        mock_storage_client_class.return_value = mock_storage
        
        # Mock document processor
        mock_doc_processor = MagicMock()
        mock_doc_processor.download_and_process.return_value = "Extracted CV text"
        mock_doc_processor_class.return_value = mock_doc_processor
        
        # Set up an error response from the Gemini client
        mock_generate_content.return_value = {
            "status": "error",
            "error": "Vertex AI error: Failed to generate content",
            "data": None
        }
        
        # Create test CV file
        with open(sample_cv_path, 'rb') as f:
            cv_file_content = f.read()
        
        cv_file = FileStorage(
            stream=io.BytesIO(cv_file_content),
            filename=sample_cv_path.name,
            content_type='application/pdf'
        )
        
        # Build the request
        request_data = {'task': 'parsing'}
        request_files = {'cv_file': cv_file}
        request_headers = {
            'Authorization': 'Bearer mock-token',
            'Content-Type': 'multipart/form-data; boundary=---testboundary'
        }
        
        request = self._build_request(request_data, files=request_files, headers=request_headers)

        # Call the function
        response = main.cv_optimizer(request)
        
        # Assertions for error case
        assert response.status_code == 500
        response_data = json.loads(response.data)
        assert "error" in response_data
        assert "Vertex AI error" in response_data["error"]
        
        # Verify our mocks were called correctly
        mock_verify_jwt.assert_called_once()
        mock_doc_processor_class.assert_called_once()
        mock_doc_processor.download_and_process.assert_called_once()
        mock_aiplatform_init.assert_called_once()
        mock_generate_content.assert_called_once()


"""
# E2E Test Outline (Not Implemented)

def test_e2e_parsing_request():
    '''
    E2E test for parsing a CV through the deployed API.
    
    This would require:
    1. A deployed function URL
    2. Valid JWT token
    3. Sample files to upload
    
    Implementation would look like:
    
    ```python
    import requests
    
    # Configuration
    base_url = "https://your-deployed-function-url.com/cv_optimizer"
    jwt_token = "your-valid-jwt-token"
    
    # Prepare files
    files = {
        'cv_file': ('sample_cv.pdf', open('tests/fixtures/sample_cv.pdf', 'rb'), 'application/pdf')
    }
    
    # Make request
    response = requests.post(
        base_url,
        data={'task': 'parsing'},
        files=files,
        headers={'Authorization': f'Bearer {jwt_token}'}
    )
    
    # Assertions
    assert response.status_code == 200
    response_data = response.json()
    assert 'name' in response_data
    assert 'email' in response_data
    assert 'skills' in response_data
    ```
    '''
    pass
""" 