import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get Supabase credentials
supabase_url = os.getenv("SUPABASE_URL")
supabase_anon_key = os.getenv("SUPABASE_ANON_KEY")
api_base_url = os.getenv("API_BASE_URL")

# Create Postman environment
postman_env = {
    "id": "cv-optimizer-env",
    "name": "CV Optimizer Environment",
    "values": [
        {
            "key": "supabase_url",
            "value": supabase_url,
            "type": "default",
            "enabled": True
        },
        {
            "key": "supabase_anon_key",
            "value": supabase_anon_key,
            "type": "secret",
            "enabled": True
        },
        {
            "key": "api_base_url",
            "value": api_base_url,
            "type": "default",
            "enabled": True
        }
    ],
    "_postman_variable_scope": "environment"
}

# Save to file
with open("cv-optimizer.postman_environment.json", "w") as f:
    json.dump(postman_env, f, indent=2)

print("Postman environment file created: cv-optimizer.postman_environment.json")
print("\nTo use this in Postman:")
print("1. Open Postman")
print("2. Click 'Import'")
print("3. Select the generated 'cv-optimizer.postman_environment.json' file")
print("4. Click 'Import'")
print("\nTo make authenticated requests:")
print("1. Create a new request")
print("2. Set the URL to: {{api_base_url}}/cv_optimizer")
print("3. Add header: Authorization: Bearer {{supabase_anon_key}}")
print("4. Send your request with the appropriate body") 