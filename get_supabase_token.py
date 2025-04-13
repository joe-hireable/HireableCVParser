from supabase import create_client
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Supabase client
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_ANON_KEY")

if not supabase_url or not supabase_key:
    print("Error: SUPABASE_URL and SUPABASE_ANON_KEY must be set in .env file")
    exit(1)

supabase = create_client(supabase_url, supabase_key)

# Get email and password from environment variables or prompt user
email = os.getenv("SUPABASE_EMAIL")
password = os.getenv("SUPABASE_PASSWORD")

if not email:
    email = input("Enter your Supabase email: ")
if not password:
    password = input("Enter your Supabase password: ")

try:
    # Sign in
    data = supabase.auth.sign_in_with_password({
        "email": email,
        "password": password
    })

    # Get the access token
    access_token = data.session.access_token
    print("\nAuthentication successful!")
    print("\nUse this token in Postman:")
    print(f"Authorization: Bearer {access_token}")
    
    # Also save to a file for easy copying
    with open("supabase_token.txt", "w") as f:
        f.write(f"Bearer {access_token}")
    print("\nToken also saved to supabase_token.txt")
    
except Exception as e:
    print(f"Error: {str(e)}") 