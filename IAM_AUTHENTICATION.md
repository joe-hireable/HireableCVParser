# IAM Authentication for CV Optimizer Function

This guide explains how to use IAM authentication with the CV Optimizer Cloud Function.

## Authentication Methods

The function now supports two authentication methods:

1. **GCP IAM Authentication** - For service accounts and GCP-managed identities
2. **Supabase JWT Authentication** - For web clients (fallback)

## Setting Up IAM Authentication

### 1. Configure the Service Account

The function will only accept requests from service accounts that have the `cloudfunctions.invoker` role:

```bash
# Add the invoker role to the service account
gcloud functions add-iam-policy-binding cv_optimizer \
  --gen2 \
  --region=europe-west2 \
  --member=serviceAccount:YOUR_SERVICE_ACCOUNT@appspot.gserviceaccount.com \
  --role=roles/cloudfunctions.invoker

# For your frontend service account:
gcloud functions add-iam-policy-binding cv_optimizer \
  --gen2 \
  --region=europe-west2 \
  --member=serviceAccount:YOUR_FRONTEND_SERVICE@appspot.gserviceaccount.com \
  --role=roles/cloudfunctions.invoker
```

### 2. Authenticate API Requests

When making requests from a service account, you need to:

1. Generate an access token for the service account
2. Include the token in the `Authorization` header

## Example Code (Python)

```python
import google.auth
import google.auth.transport.requests
import requests

# Get credentials for the default service account
credentials, project = google.auth.default()
auth_req = google.auth.transport.requests.Request()
credentials.refresh(auth_req)
token = credentials.token

# Call the function with the token
response = requests.post(
    "https://cv-optimizer-jfhhzkvnca-nw.a.run.app", 
    headers={"Authorization": f"Bearer {token}"},
    data={"task": "parsing"}
)
```

## Example with Frontend Integration

For a frontend app using Google Cloud, you have two options:

### Option 1: Client-side Authentication

If your frontend runs on Firebase or App Engine, use the Identity Platform to get a token:

```javascript
// Using Firebase Authentication
import { getAuth, getIdToken } from "firebase/auth";

async function callCVOptimizerFunction() {
  const auth = getAuth();
  const token = await getIdToken(auth.currentUser);
  
  const response = await fetch("https://cv-optimizer-jfhhzkvnca-nw.a.run.app", {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${token}`
    },
    body: formData
  });
  
  return await response.json();
}
```

### Option 2: Backend Proxy

Use a backend service with a service account to proxy requests to the function:

```javascript
// Frontend calls your backend proxy
async function callBackendProxy() {
  const response = await fetch("/api/cv-optimizer", {
    method: "POST",
    body: formData
  });
  
  return await response.json();
}
```

And on your backend proxy:

```python
# Backend proxy with service account authentication
@app.route("/api/cv-optimizer", methods=["POST"])
def proxy_to_cv_optimizer():
    # Get service account token
    credentials, _ = google.auth.default()
    auth_req = google.auth.transport.requests.Request()
    credentials.refresh(auth_req)
    token = credentials.token
    
    # Forward the request
    response = requests.post(
        "https://cv-optimizer-jfhhzkvnca-nw.a.run.app",
        headers={"Authorization": f"Bearer {token}"},
        data=request.form,
        files=request.files
    )
    
    return jsonify(response.json())
```

## Testing IAM Authentication

Use the included `test_iam_auth.py` script to test authentication:

```bash
python test_iam_auth.py
```

## Troubleshooting

If you encounter authentication issues:

1. **401 Unauthorized** - Check that the service account has the `cloudfunctions.invoker` role
2. **403 Forbidden** - Check that the token is valid and not expired
3. **Check logs** - Look at Cloud Functions logs for detailed authentication errors 