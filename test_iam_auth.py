import requests
import json
import os
import subprocess
import google.auth
import google.auth.transport.requests
import pytest

def get_service_account_token():
    """Get an access token for the default service account."""
    try:
        credentials, project = google.auth.default()
        auth_req = google.auth.transport.requests.Request()
        credentials.refresh(auth_req)
        return credentials.token
    except Exception as e:
        pytest.skip(f"No valid service account credentials available: {str(e)}")
        return None

def test_function_with_service_account():
    """Test calling the function with a service account token."""
    # Get the Cloud Function URL from environment or use a default
    function_url = os.environ.get('API_BASE_URL', 'https://cv-optimizer-jfhhzkvnca-nw.a.run.app')
    
    # Get a token for the service account
    token = get_service_account_token()
    if token is None:
        pytest.skip("Skipping test as no valid service account token could be obtained")
    
    # Basic health check endpoint
    endpoint = f"{function_url}"
    
    headers = {
        'Authorization': f'Bearer {token}'
    }
    
    response = requests.get(endpoint, headers=headers)
    
    print(f"Status code: {response.status_code}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except:
        print(f"Response text: {response.text}")
    
    print(f"Headers: {response.headers}")

if __name__ == "__main__":
    test_function_with_service_account() 