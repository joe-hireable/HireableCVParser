import os
import jwt
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get Supabase project details from environment
jwt_secret = os.getenv("SUPABASE_JWT_SECRET")
project_ref = os.getenv("SUPABASE_PROJECT_REF")

if not jwt_secret or not project_ref:
    print("Error: SUPABASE_JWT_SECRET and SUPABASE_PROJECT_REF must be set in .env file")
    exit(1)

def generate_test_token(
    user_id="test-user-id",
    email="test@example.com",
    expiry_seconds=3600,
    role="authenticated"
):
    """Generate a test JWT token for testing purposes."""
    # Create the token payload with all required claims
    current_time = int(time.time())
    payload = {
        "sub": user_id,
        "email": email,
        "role": role,
        "iat": current_time,
        "exp": current_time + expiry_seconds,
        "iss": f"https://{project_ref}.supabase.co/auth/v1",
        "aud": "authenticated"
    }
    
    # Sign the token with the secret
    token = jwt.encode(
        payload,
        jwt_secret,
        algorithm="HS256"
    )
    
    return token

# Generate a token
token = generate_test_token()

# Print the token for use in Postman
print("\nToken for Postman:")
print(f"Authorization: Bearer {token}")

# Save to a file for easy copying
with open("test_token.txt", "w") as f:
    f.write(f"Bearer {token}")
print("\nToken also saved to test_token.txt") 