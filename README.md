# CV Optimizer Cloud Function

A Google Cloud Function that uses Gemini 2.0 to analyze, optimize, and provide insights for CVs (resumes) based on job descriptions.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
- [API Usage](#api-usage)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Deployment](#deployment)
- [Testing](#testing)

## 🔍 Overview

This cloud function serves as an API for CV (resume) optimization and analysis using Google's Gemini 2.0 models. It can parse CVs, analyze them against job descriptions, and provide actionable feedback and optimization suggestions.

## ✨ Features

- **CV Parsing**: Extract structured data from uploaded CV documents (PDF or DOCX)
- **Personal Statement Analysis**: Review and improve personal statements/profiles
- **Key Achievements Analysis**: Analyze and enhance key achievements
- **Core Skills Analysis**: Identify and optimize core skills sections
- **Role Analysis**: Evaluate role descriptions and experience
- **CV Scoring**: Score CVs against job descriptions for compatibility
- **OpenTelemetry Integration**: Built-in tracing and monitoring
- **Supabase Authentication**: JWT-based authentication for secure API access
- **Google ADK Integration**: Support for complex, stateful interactions via Google Agent Development Kit
- **Secret Manager Integration**: Secure storage for prompts, schemas, and examples
- **Multipart Form Support**: File uploads directly via multipart/form-data
- **Structured Logging**: JSON-formatted logs for better debugging

## 📋 Prerequisites

- Python 3.11 or higher
- Google Cloud Platform account with billing enabled
- Gemini API access (via Google Cloud AI Platform)
- Google Cloud SDK installed (for deployment)
- Supabase project (for authentication)
- (Optional) Google ADK agent configured

## 🚀 Getting Started

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd cvai2
   ```

2. **Set up a virtual environment**
   ```bash
   # On Windows
   python -m venv venv311
   .\venv311\Scripts\activate

   # On macOS/Linux
   python -m venv venv311
   source venv311/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # For development dependencies
   ```

4. **Set up environment variables**
   ```bash
   # Copy the template file
   cp .env.template .env
   
   # Edit the .env file with your values
   ```

5. **Set up Google Cloud credentials**
   ```bash
   # On Windows (PowerShell)
   $env:GOOGLE_APPLICATION_CREDENTIALS="path/to/your/credentials.json"

   # On macOS/Linux
   export GOOGLE_APPLICATION_CREDENTIALS="path/to/your/credentials.json"
   ```

6. **Start the function locally**
   ```bash
   functions-framework --target=cv_optimizer
   ```

## 📡 API Usage

### Authentication

The API supports two authentication methods:

1. **Supabase JWT Authentication** (For web clients)
   ```
   Authorization: Bearer <your-supabase-jwt-token>
   ```

2. **GCP IAM Authentication** (For service accounts and GCP services)
   Generate an access token for your service account and include it in the Authorization header:
   ```
   Authorization: Bearer <your-service-account-token>
   ```
   See [IAM_AUTHENTICATION.md](IAM_AUTHENTICATION.md) for detailed setup instructions.

### Endpoint

`POST https://YOUR_FUNCTION_URL`

### Request Format

The API accepts `multipart/form-data` with the following fields:

- `cv_file`: The CV document file (PDF or DOCX)
- `task`: The task to perform (`parsing`, `ps`, `cs`, `ka`, `role`, `scoring`)
- `jd`: (Optional) Job description text or URL
- `section`: (Optional) Specific section to analyze
- `model`: (Optional) Gemini model to use (defaults to `gemini-2.0-flash-001`)

Example cURL request:
```bash
curl -X POST https://YOUR_FUNCTION_URL \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "X-Request-ID: unique-request-id" \
  -F "cv_file=@/path/to/your/cv.pdf" \
  -F "task=parsing" \
  -F "model=gemini-2.0-flash-001"
```

## 📂 Project Structure

```
root/
├── main.py                  # Main function code
├── config.py                # Configuration settings
├── requirements.txt         # Python dependencies
├── requirements-dev.txt     # Development dependencies
├── .gitignore               # Git ignore file
├── .gcloudignore            # GCloud ignore file
├── utils/                   # Utility modules
│   ├── __init__.py
│   ├── document_processor.py  # Document handling
│   ├── storage.py             # GCS operations
│   ├── gemini_client.py       # Gemini API client
│   ├── adk_client.py          # ADK integration
│   └── secret_manager.py      # Secret Manager client
├── models/                  # Data models
│   └── schemas.py           # Pydantic schemas
├── data/                    # Resource files
│   ├── prompts/             # Prompt templates
│   ├── schemas/             # JSON output schemas
│   └── few_shot_examples/   # Example data for model training
├── tests/                   # Test files
│   ├── test_api.py          # API endpoint tests
│   ├── test_iam_auth.py     # IAM authentication tests
│   └── test_basic.py        # Basic functionality tests
└── docs/                    # Documentation
```

## ⚙️ Configuration

Key configuration settings in `config.py`:

- **GCS_BUCKET_NAME**: Google Cloud Storage bucket for storing documents
- **PROJECT_ID**: Google Cloud Project ID
- **LOCATION**: Google Cloud region (default: europe-west9)
- **DEFAULT_MODEL**: Gemini model version to use
- **SUPPORTED_MODELS**: List of supported Gemini models
- **VERTEX_AI_ENABLED**: Whether to use Vertex AI (or direct Gemini API)
- **USE_ADK**: Whether to use Google Agent Development Kit
- **ADK_AGENT_LOCATION**: Location path to the ADK agent
- **USE_SECRETS_MANAGER**: Whether to use Secret Manager for resources
- **PROMPTS_SECRET_PREFIX**: Prefix for prompt secrets
- **SCHEMAS_SECRET_PREFIX**: Prefix for schema secrets
- **EXAMPLES_SECRET_PREFIX**: Prefix for few-shot examples secrets
- **SUPABASE_JWT_SECRET**: Secret for validating Supabase JWT tokens
- **SUPABASE_PROJECT_REF**: Supabase project reference

## 📦 Deployment

### Environment Variables
See `.env.template` for all required and optional environment variables. The following variables are required for deployment:

- `PROJECT_ID` - Your Google Cloud Project ID
- `GCS_BUCKET_NAME` - Your Google Cloud Storage bucket
- `SUPABASE_JWT_SECRET` - Your Supabase JWT secret
- `SUPABASE_PROJECT_REF` - Your Supabase project reference

### Deploying as a GCP Function

#### Option 1: Using trigger-build.bat (Windows)
```bash
.\trigger-build.bat
```

#### Option 2: Manual deployment
```bash
gcloud functions deploy cv_optimizer \
  --gen2 \
  --runtime=python311 \
  --region=europe-west2 \
  --source=. \
  --entry-point=cv_optimizer \
  --trigger-http \
  --memory=2048MB \
  --timeout=540s \
  --set-env-vars="USE_ADK=true,ADK_AGENT_LOCATION=projects/hireable-places/locations/europe-west2/agents/cv-optimizer-agent" \
  --allow-unauthenticated
```

### Docker Deployment
The project includes a Dockerfile for containerized deployment:

```bash
# Build the Docker image
docker build -t cv-optimizer .

# Run the container locally
docker run -p 8080:8080 \
  -e GOOGLE_APPLICATION_CREDENTIALS=/path/to/credentials.json \
  -v /path/to/credentials.json:/path/to/credentials.json \
  cv-optimizer
```

## 🧪 Testing

The project includes several test suites:

1. **API Tests** (`test_api.py`): Tests for API endpoints and request handling
2. **IAM Authentication Tests** (`test_iam_auth.py`): Tests for IAM authentication
3. **Basic Functionality Tests** (`test_basic.py`): Tests for core functionality

Run tests using pytest:
```bash
pytest tests/
```

For development dependencies:
```bash
pip install -r requirements-dev.txt
```

# Supabase Token Generator

A simple script to generate a Supabase authentication token for testing API endpoints in Postman.

## Setup

1. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Configure your Supabase credentials:
   - Copy the `.env` file and fill in your Supabase details:
     ```
     SUPABASE_URL=https://your-project-ref.supabase.co
     SUPABASE_ANON_KEY=your-anon-key
     SUPABASE_EMAIL=your-email@example.com
     SUPABASE_PASSWORD=your-password
     ```
   - You can find your Supabase URL and anon key in your Supabase project settings

## Usage

1. Run the script:
   ```
   python get_supabase_token.py
   ```

2. If you haven't set your email and password in the `.env` file, the script will prompt you to enter them.

3. The script will:
   - Authenticate with Supabase
   - Display the token in the console
   - Save the token to `supabase_token.txt` for easy copying

4. Use the token in Postman:
   - Add a header: `Authorization: Bearer your-token-here`

## Security Notes

- Never commit your `.env` file to version control
- The token has a limited lifespan and will need to be refreshed
- For production applications, implement proper token refresh logic 

# CV Optimizer API Testing Tool

This tool allows for comprehensive testing of the CV Optimizer API, which is part of the backend for the CV Builder 2.0 application.

## Setup

1. Make sure you have the required dependencies installed:

```bash
pip install -r requirements.txt
```

2. Create a `.env` file with the following variables:

```
SUPABASE_JWT_SECRET="your-supabase-jwt-secret"
SUPABASE_PROJECT_REF="your-supabase-project-ref"
API_BASE_URL="http://your-api-url:8080"  # Optional, defaults to localhost:8080
```

3. Ensure you have a sample CV file for testing. A sample file `sample_resume.txt` is included.

## Usage

Run the script with the desired test options:

```bash
python test_api.py [options]
```

### Available Options

- `--all`: Run all available tests
- `--parsing`: Test CV parsing functionality
- `--scoring`: Test CV scoring functionality with a job description
- `--ps`: Test personal statement generation
- `--models`: Test different model selections
- `--auth-failure`: Test authentication failure
- `--invalid-file`: Test with invalid file types
- `--token`: Generate and print a token for manual testing (default if no tests specified)
- `--url URL`: Override the API URL
- `--cv PATH`: Specify a custom CV file path for testing

### Examples

1. Generate a JWT token for manual testing:

```bash
python test_api.py --token
```

2. Test CV parsing with a custom CV file:

```bash
python test_api.py --parsing --cv path/to/your/cv.pdf
```

3. Test against a specific API endpoint:

```bash
python test_api.py --all --url https://your-api-endpoint.com
```

4. Test just the personal statement generation:

```bash
python test_api.py --ps
```

## Response Structure

Each test validates that the API response matches the expected structure:

- CV Parsing: Should return `cv_data` with `contact_info` and other structured CV information
- CV Scoring: Should return `scores` with matching metrics for the resume against the job description
- Personal Statement: Should return `personal_statement` with a tailored personal statement
- Error cases: Should return appropriate status codes and error messages

## Supported CV File Formats

The API supports the following CV file formats:
- Plain text (`.txt`)
- PDF (`.pdf`)
- Microsoft Word (`.docx`)

## Error Testing

The script can test various error conditions:
- Authentication failures (invalid/expired tokens)
- Invalid file types
- Invalid model names
- Missing required parameters

## Adding New Tests

You can extend the test suite by adding new functions that use the `make_api_request` helper function and adding appropriate command-line arguments in the `main()` function. 