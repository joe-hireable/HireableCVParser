import json
import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path
import functions_framework
from werkzeug.datastructures import FileStorage, Headers
import io
from flask import Request, Flask
from werkzeug.test import EnvironBuilder
import google.cloud.aiplatform as aiplatform
from vertexai.generative_models import GenerativeModel as VertexGenerativeModel

# Import main application module (assuming it's structured like this)
import main
from models.schemas import ParsingResponseSchema, ScoringResponseSchema
from models.schemas import ParsingDataModel, SkillModel, SkillProficiencyEnum, SkillTypeEnum, ExperienceModel, EducationModel, LocationModel
from models.schemas import ScoresModel, FeedbackModel, ScoringDataModel

# Create a test Flask app for application context
# Use a function to create the app to prevent pytest from collecting it
@pytest.fixture(scope='session')
def test_app():
    app = Flask(__name__)
    return app

# Mock resource loading function
def mock_load_resource_file(task, resource_type):
    if resource_type == 'system_prompt':
        return "Mock system prompt"
    elif resource_type == 'user_prompt':
        return f"Mock user prompt for {task} with {{cv_content}}, {{jd_content}}, {{few_shot_examples}}"
    elif resource_type == 'schema':
        # Return a valid JSON schema with required fields
        return json.dumps({
            "type": "object",
            "properties": {
                "status": {"type": "string"},
                "data": {"type": "object"}
            },
            "required": ["status", "data"],
            "$defs": {}
        })
    elif resource_type == 'examples':
        return "Mock few shot examples"
    return None

# Mock validate_request_headers function
def mock_validate_request_headers(request):
    """Mock function that always returns None, indicating headers are valid"""
    return None

class TestMainFlow:
    """Integration tests for the main application flow."""
    
    @pytest.fixture(autouse=True)
    def setup_app_context(self, test_app):
        """Setup Flask application context for all tests."""
        with test_app.app_context():
            yield
    
    def _build_request(self, data, files=None, headers=None, method='POST'):
        """Helper function to build a Flask Request object."""
        # If no headers provided, create empty headers
        if headers is None:
            headers = {}
        
        # Ensure X-Request-ID is present to pass validation
        if 'X-Request-ID' not in headers:
            headers['X-Request-ID'] = 'test-request-id'
        
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
    
    def _call_function(self, request, test_app):
        """
        Call the cloud function with proper application context.
        This wraps the main.cv_optimizer function with the necessary Flask context.
        """
        with test_app.app_context():
            # Patch validate_request_headers within the scope of this function call
            with patch('main.validate_request_headers', side_effect=mock_validate_request_headers):
                return main.cv_optimizer(request)

    @patch("main.load_resource_file", side_effect=mock_load_resource_file)
    @patch("main.validate_jwt")
    @patch("main.DocumentProcessor")
    @patch("main.StorageClient")
    @patch("google.cloud.aiplatform.init")
    @patch("vertexai.generative_models.GenerativeModel")
    @patch("utils.gemini_client.GeminiClient.generate_content")
    def test_parsing_request(self, mock_generate_content, mock_vertex_model, mock_aiplatform_init,
                          mock_storage_client_class, mock_doc_processor_class,
                          mock_verify_jwt, mock_loader, sample_cv_path, test_app):
        """Test the parsing task flow through the API with Vertex AI."""
        # Configure mocks
        mock_verify_jwt.return_value = {'sub': 'mock-user-id'}

        # Mock Storage Client
        mock_storage = MagicMock()
        mock_storage.save_bytes_to_gcs.return_value = "gs://mock-bucket/mock_cv.pdf"
        mock_storage_client_class.return_value = mock_storage

        # Mock document processor
        mock_doc_processor = MagicMock()
        mock_doc_processor.process_document.return_value = {
            "status": "success",
            "data": {
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
                    }
                ],
                "achievements": ["Achievement 1"],
                "experience": [
                    {
                        "company": "Tech Innovations Ltd",
                        "title": "Senior Software Engineer",
                        "start": "January 2021",
                        "current": True,
                        "summary": "Working on cloud solutions",
                        "highlights": ["Task 1"]
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
        }
        mock_doc_processor_class.return_value = mock_doc_processor

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
            'Content-Type': 'multipart/form-data; boundary=---testboundary',
            'X-Request-ID': 'test-request-id'
        }

        request = self._build_request(request_data, files=request_files, headers=request_headers)

        # Call the function using our wrapper with app context
        response = self._call_function(request, test_app)

        # Assertions
        assert response.status_code == 200
        response_data = json.loads(response.data)
        assert response_data["result"]["status"] == "success"
        assert response_data["result"]["data"]["firstName"] == "John"

    @patch("main.load_resource_file", side_effect=mock_load_resource_file)
    @patch("main.validate_jwt")
    @patch("main.DocumentProcessor")
    @patch("main.StorageClient")
    @patch("google.cloud.aiplatform.init")
    @patch("vertexai.generative_models.GenerativeModel")
    @patch("utils.gemini_client.GeminiClient.generate_content")
    def test_scoring_request(self, mock_generate_content, mock_vertex_model, mock_aiplatform_init,
                           mock_storage_client_class, mock_doc_processor_class,
                           mock_verify_jwt, mock_loader,
                           sample_cv_path, sample_jd_path, test_app):
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
        mock_doc_processor.process_document.return_value = {
            "status": "success",
            "data": mock_scoring_data
        }
        mock_doc_processor_class.return_value = mock_doc_processor

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
            'Content-Type': 'multipart/form-data; boundary=---testboundary',
            'X-Request-ID': 'test-request-id'
        }

        request = self._build_request(request_data, files=request_files, headers=request_headers)

        # Call the function using our wrapper with app context
        response = self._call_function(request, test_app)

        # Assertions
        assert response.status_code == 200
        response_data = json.loads(response.data)
        assert response_data["result"]["status"] == "success"
        assert response_data["result"]["data"]["scores"]["overall"] == 85

    @patch("main.load_resource_file", side_effect=mock_load_resource_file)
    @patch("main.validate_jwt")
    @patch("main.DocumentProcessor")
    @patch("main.StorageClient")
    @patch("google.cloud.aiplatform.init")
    @patch("vertexai.generative_models.GenerativeModel")
    @patch("utils.gemini_client.GeminiClient.generate_content")
    def test_error_handling(self, mock_generate_content, mock_vertex_model, mock_aiplatform_init,
                          mock_storage_client_class, mock_doc_processor_class,
                          mock_verify_jwt, mock_loader, sample_cv_path, test_app):
        """Test error handling in the API with Vertex AI."""
        # Configure mocks
        mock_verify_jwt.return_value = {'sub': 'mock-user-id'}

        # Mock Storage Client
        mock_storage = MagicMock()
        mock_storage.save_bytes_to_gcs.return_value = "gs://mock-bucket/mock_cv.pdf"
        mock_storage_client_class.return_value = mock_storage

        # Mock document processor to raise an error
        mock_doc_processor = MagicMock()
        mock_doc_processor.process_document.side_effect = Exception("Vertex AI error: Failed to generate content")
        mock_doc_processor_class.return_value = mock_doc_processor

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
            'Content-Type': 'multipart/form-data; boundary=---testboundary',
            'X-Request-ID': 'test-request-id'
        }

        request = self._build_request(request_data, files=request_files, headers=request_headers)

        # Call the function using our wrapper with app context
        response = self._call_function(request, test_app)

        # Assertions for error case
        assert response.status_code == 500
        response_data = json.loads(response.data)
        assert "error" in response_data
        assert "Vertex AI error" in response_data["error"]


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