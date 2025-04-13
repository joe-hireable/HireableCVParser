import os
import pytest
import requests
import json
from pathlib import Path
import sys

# Add the root directory to Python path to import test_api
sys.path.append(str(Path(__file__).parent.parent.parent))
from test_api import generate_test_token

# Get the deployed function URL from environment or use the default
FUNCTION_URL = os.getenv(
    'CV_OPTIMIZER_URL',
    'https://europe-west2-hireable-places.cloudfunctions.net/cv_optimizer'
)

@pytest.fixture
def auth_token():
    """Generate a valid test token for authentication."""
    return generate_test_token(
        user_id="test-user-123",
        email="test@example.com",
        expiry_seconds=3600
    )

def test_parsing_request(auth_token):
    """Test the parsing task on the deployed function."""
    print(f"\nTesting parsing request against URL: {FUNCTION_URL}")
    
    # Get the path to the sample CV file
    sample_cv_path = Path(__file__).parent.parent / 'fixtures' / 'sample_cv.pdf'
    assert sample_cv_path.exists(), f"Sample CV file not found at {sample_cv_path}"
    print(f"Using sample CV file: {sample_cv_path}")
    
    try:
        # Prepare the files for upload
        files = {
            'cv_file': ('sample_cv.pdf', open(sample_cv_path, 'rb'), 'application/pdf')
        }
        
        # Make request to the deployed function
        print("Making POST request for parsing task...")
        response = requests.post(
            FUNCTION_URL,
            data={'task': 'parsing'},
            files=files,
            headers={'Authorization': f'Bearer {auth_token}'},
            timeout=30  # Add timeout
        )
        
        # Print response details
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {json.dumps(dict(response.headers), indent=2)}")
        print(f"Response Body: {response.text[:1000]}...")  # First 1000 chars
        
        # Basic assertions
        assert response.status_code in [200, 401], f"Unexpected status code: {response.status_code}"
        
        if response.status_code == 200:
            response_data = response.json()
            # Verify the response has the expected structure
            assert 'name' in response_data, "Response missing 'name' field"
            assert 'email' in response_data, "Response missing 'email' field"
            assert 'skills' in response_data, "Response missing 'skills' field"
            
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Request failed: {str(e)}")
    except json.JSONDecodeError as e:
        pytest.fail(f"Failed to parse JSON response: {str(e)}")
    except Exception as e:
        pytest.fail(f"Unexpected error: {str(e)}")

def test_scoring_request(auth_token):
    """Test the scoring task on the deployed function."""
    print(f"\nTesting scoring request against URL: {FUNCTION_URL}")
    
    # Get the paths to the sample files
    sample_cv_path = Path(__file__).parent.parent / 'fixtures' / 'sample_cv.pdf'
    sample_jd_path = Path(__file__).parent.parent / 'fixtures' / 'sample_jd.pdf'
    
    assert sample_cv_path.exists(), f"Sample CV file not found at {sample_cv_path}"
    assert sample_jd_path.exists(), f"Sample JD file not found at {sample_jd_path}"
    print(f"Using sample CV file: {sample_cv_path}")
    print(f"Using sample JD file: {sample_jd_path}")
    
    try:
        # Prepare the files for upload
        files = {
            'cv_file': ('sample_cv.pdf', open(sample_cv_path, 'rb'), 'application/pdf'),
            'jd_file': ('sample_jd.pdf', open(sample_jd_path, 'rb'), 'application/pdf')
        }
        
        # Make request to the deployed function
        print("Making POST request for scoring task...")
        response = requests.post(
            FUNCTION_URL,
            data={'task': 'scoring'},
            files=files,
            headers={'Authorization': f'Bearer {auth_token}'},
            timeout=30  # Add timeout
        )
        
        # Print response details
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {json.dumps(dict(response.headers), indent=2)}")
        print(f"Response Body: {response.text[:1000]}...")  # First 1000 chars
        
        # Basic assertions
        assert response.status_code in [200, 401], f"Unexpected status code: {response.status_code}"
        
        if response.status_code == 200:
            response_data = response.json()
            # Verify the response has the expected structure
            assert 'overall_score' in response_data, "Response missing 'overall_score' field"
            assert 'strengths' in response_data, "Response missing 'strengths' field"
            assert 'weaknesses' in response_data, "Response missing 'weaknesses' field"
            
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Request failed: {str(e)}")
    except json.JSONDecodeError as e:
        pytest.fail(f"Failed to parse JSON response: {str(e)}")
    except Exception as e:
        pytest.fail(f"Unexpected error: {str(e)}") 