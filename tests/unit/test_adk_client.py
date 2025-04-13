"""Unit tests for ADK client."""

import json
from unittest.mock import patch, MagicMock
import pytest

# Mock the adk import before importing ADKClient
with patch("utils.adk_client.adk") as mock_adk_module:
    from utils.adk_client import ADKClient

@pytest.fixture
def mock_adk():
    """Mock ADK module."""
    with patch("utils.adk_client.adk") as mock:
        yield mock

@pytest.fixture
def mock_agent(mock_adk):
    """Mock ADK agent."""
    mock_agent = MagicMock()
    mock_adk.Agent.return_value = mock_agent
    return mock_agent

class TestADKClient:
    """Test cases for ADKClient."""

    def test_initialization(self, mock_adk, mock_agent):
        """Test ADK client initialization."""
        # Initialize client
        client = ADKClient(
            agent_location="projects/test-project-id/locations/us-central1/agents/test-agent-id"
        )

        # Verify agent was created
        mock_adk.Agent.assert_called_once_with(
            agent_name="projects/test-project-id/locations/us-central1/agents/test-agent-id"
        )
        assert client.agent == mock_agent

    def test_cleanup(self, mock_adk, mock_agent):
        """Test ADK client cleanup."""
        # Initialize and cleanup client
        client = ADKClient(
            agent_location="projects/test-project-id/locations/us-central1/agents/test-agent-id"
        )
        client.cleanup()

        # Verify agent was cleaned up
        assert client.agent is None

    @patch("utils.adk_client.ADK_AVAILABLE", True)
    @patch("utils.adk_client.SCHEMA_REGISTRY")
    def test_process_cv(self, mock_schema_registry, mock_adk, mock_agent):
        """Test processing a CV with ADK."""
        # Setup a mock schema that simply returns the input data
        class MockSchema:
            def model_validate(self, data):
                return data
                
        mock_schema_registry.get.return_value = MockSchema()
        
        # Setup mocks with a simple response
        mock_session = MagicMock()
        mock_agent.start_session.return_value = mock_session
        mock_session.execute.return_value = MagicMock(
            structured_response=json.dumps({
                "status": "success",
                "data": {
                    "firstName": "John",
                    "surname": "Doe",
                    "email": "john.doe@example.com"
                }
            })
        )

        # Initialize client and process CV
        client = ADKClient(
            agent_location="projects/test-project-id/locations/us-central1/agents/test-agent-id"
        )
        result = client.process_cv("CV text content", "parsing")

        # Verify agent processed the CV
        mock_agent.start_session.assert_called_once()
        call_args = mock_agent.start_session.call_args[0][0]
        assert call_args["cv_content"] == "CV text content"
        assert call_args["task"] == "parsing"
        assert call_args["jd_content"] == ""
        assert call_args["section"] == ""

        # Check result
        assert result["status"] == "success"
        assert "data" in result
        data = result["data"]
        assert data["firstName"] == "John"
        assert data["surname"] == "Doe"
        assert data["email"] == "john.doe@example.com"

    def test_process_cv_document_error(self, mock_adk, mock_agent):
        """Test handling document processing errors."""
        # Initialize client and process CV with None content
        client = ADKClient(
            agent_location="projects/test-project-id/locations/us-central1/agents/test-agent-id"
        )
        result = client.process_cv(None, "parsing")

        # Verify error response
        assert result["status"] == "error"
        assert "CV content cannot be None" in result["error"]
        assert result["data"] is None

    def test_process_cv_agent_error(self, mock_adk, mock_agent):
        """Test handling agent processing errors."""
        # Setup mock to raise an exception
        mock_agent.start_session.side_effect = Exception("ADK error")

        # Initialize client and process CV
        client = ADKClient(
            agent_location="projects/test-project-id/locations/us-central1/agents/test-agent-id"
        )
        result = client.process_cv("CV text content", "parsing")

        # Verify error response
        assert result["status"] == "error"
        assert "ADK error" in result["error"]
        assert result["data"] is None

    @patch("utils.adk_client.SCHEMA_REGISTRY")
    def test_process_cv_with_schema(self, mock_schema_registry, mock_adk, mock_agent):
        """Test processing CV with schema validation."""
        # Setup schema mock
        class MockSchema:
            def model_validate(self, data):
                # Return a mock object with model_dump method
                mock_validated = MagicMock()
                mock_validated.model_dump.return_value = {
                    "firstName": "John",
                    "surname": "Doe",
                    "email": "john.doe@example.com",
                    "phone": "+44 7700 900000",
                    "links": ["https://linkedin.com/in/johndoe"],
                    "location": "London, UK",
                    "headline": "Senior Software Engineer",
                    "profileStatement": "Experienced software engineer",
                    "skills": ["Python", "JavaScript"],
                    "achievements": ["Led team of 5"],
                    "languages": ["English"],
                    "experience": [
                        {
                            "company": "Tech Corp",
                            "role": "Senior Developer",
                            "dates": "2020-Present",
                            "responsibilities": ["Led development team"]
                        }
                    ],
                    "education": [
                        {
                            "institution": "University of London",
                            "qualification": "BSc Computer Science",
                            "dates": "2012-2016"
                        }
                    ],
                    "certifications": ["AWS Certified"],
                    "professionalMemberships": ["IEEE"],
                    "publications": ["Technical Blog Posts"],
                    "additionalDetails": "Open source contributor"
                }
                return mock_validated

        mock_schema_registry.get.return_value = MockSchema()

        # Setup agent mock with a response that matches the schema
        mock_session = MagicMock()
        mock_agent.start_session.return_value = mock_session
        mock_session.execute.return_value = MagicMock(
            structured_response=json.dumps({
                "status": "success",
                "data": {
                    "firstName": "John",
                    "surname": "Doe",
                    "email": "john.doe@example.com",
                    "phone": "+44 7700 900000",
                    "links": ["https://linkedin.com/in/johndoe"],
                    "location": "London, UK",
                    "headline": "Senior Software Engineer",
                    "profileStatement": "Experienced software engineer",
                    "skills": ["Python", "JavaScript"],
                    "achievements": ["Led team of 5"],
                    "languages": ["English"],
                    "experience": [
                        {
                            "company": "Tech Corp",
                            "role": "Senior Developer",
                            "dates": "2020-Present",
                            "responsibilities": ["Led development team"]
                        }
                    ],
                    "education": [
                        {
                            "institution": "University of London",
                            "qualification": "BSc Computer Science",
                            "dates": "2012-2016"
                        }
                    ],
                    "certifications": ["AWS Certified"],
                    "professionalMemberships": ["IEEE"],
                    "publications": ["Technical Blog Posts"],
                    "additionalDetails": "Open source contributor"
                }
            })
        )

        # Initialize client and process CV
        client = ADKClient(
            agent_location="projects/test-project-id/locations/us-central1/agents/test-agent-id"
        )
        result = client.process_cv("CV text content", "parsing")

        # Verify schema was used
        mock_schema_registry.get.assert_called_once_with("parsing")

        # Check result
        assert result["status"] == "success"
        assert "data" in result
        data = result["data"]
        assert data["firstName"] == "John"
        assert data["surname"] == "Doe"
        assert data["email"] == "john.doe@example.com"

    def test_process_cv_invalid_json(self, mock_adk, mock_agent):
        """Test handling invalid JSON response."""
        # Setup mock with invalid JSON response
        mock_session = MagicMock()
        mock_agent.start_session.return_value = mock_session
        mock_session.execute.return_value = MagicMock(
            structured_response="Invalid JSON",
            response="Invalid JSON"
        )

        # Initialize client and process CV
        client = ADKClient(
            agent_location="projects/test-project-id/locations/us-central1/agents/test-agent-id"
        )
        result = client.process_cv("CV text content", "parsing")

        # Verify error response
        assert result["status"] == "error"
        assert "Invalid JSON response" in result["error"]
        assert result["data"] == "Invalid JSON"

    # TODO: Add more tests for handling specific tasks
    # TODO: Add tests for error handling
    # TODO: Add tests for retries and rate limiting 