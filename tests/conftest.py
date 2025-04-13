import os
import pytest
from unittest.mock import MagicMock
from pathlib import Path


@pytest.fixture
def sample_cv_path():
    """Return the path to a sample CV file for testing."""
    return Path(__file__).parent / "fixtures" / "sample_cv.pdf"


@pytest.fixture
def sample_jd_path():
    """Return the path to a sample job description file for testing."""
    return Path(__file__).parent / "fixtures" / "sample_jd.txt"


@pytest.fixture
def real_cv_paths():
    """Return a list of paths to real CV PDF files for testing."""
    cv_dir = Path(__file__).parent / "fixtures" / "cv_pdfs"
    return list(cv_dir.glob("*.pdf"))


@pytest.fixture
def real_cv_path():
    """Return a single real CV PDF path for testing."""
    cv_dir = Path(__file__).parent / "fixtures" / "cv_pdfs"
    cv_files = list(cv_dir.glob("*.pdf"))
    if cv_files:
        return cv_files[0]
    else:
        raise FileNotFoundError("No CV PDFs found in fixtures/cv_pdfs directory")


@pytest.fixture
def mock_supabase_jwt():
    """Return a mock JWT token for testing."""
    return "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"


@pytest.fixture
def mock_storage_client():
    """Mock the GCS storage client."""
    mock_client = MagicMock()
    return mock_client


@pytest.fixture
def mock_secret_manager_client():
    """Mock the Secret Manager client."""
    mock_client = MagicMock()
    # Configure the mock to return appropriate values for get_secret calls
    mock_client.get_secret.return_value = "mock_secret_value"
    return mock_client


@pytest.fixture
def mock_gemini_client():
    """Mock the Gemini client."""
    mock_client = MagicMock()
    # Configure the mock to return appropriate values for generate_content calls
    mock_response = MagicMock()
    mock_response.text = """{"role": "ATS Specialist", "keyPoints": ["Example key point 1", "Example key point 2"]}"""
    mock_client.generate_content.return_value = mock_response
    return mock_client


@pytest.fixture
def mock_adk_client():
    """Mock the ADK client."""
    mock_client = MagicMock()
    # Configure the mock to return appropriate values for call_agent
    mock_client.call_agent.return_value = {
        "role": "Software Engineer",
        "keyPoints": ["Strong Python experience", "Cloud expertise"]
    }
    return mock_client


@pytest.fixture
def mock_flask_request():
    """Create a mock Flask request object."""
    class MockRequest:
        def __init__(self):
            self.headers = {"Authorization": "Bearer mock_token"}
            self.files = {}
            self.form = {}
            
        def get_json(self):
            return {}
            
    return MockRequest() 