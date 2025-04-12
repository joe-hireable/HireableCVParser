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
- [New Features](#new-features)
- [Deployment](#deployment)
- [Migration Guide](#migration-guide)

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
   python -m venv venv
   .\venv\Scripts\activate

   # On macOS/Linux
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Copy the template file
   cp .env.template .env
   
   # Edit the .env file with your values
   # Required:
   # - PROJECT_ID, LOCATION, GCS_BUCKET_NAME
   # - SUPABASE_JWT_SECRET, SUPABASE_PROJECT_REF (for auth)
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

The API requires a Supabase JWT token in the Authorization header:

```
Authorization: Bearer <your-supabase-jwt-token>
```

### Endpoint

`POST https://YOUR_FUNCTION_URL`

### Request Format

The API now accepts `multipart/form-data` with the following fields:

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
├── .gitignore               # Git ignore file
├── .gcloudignore            # GCloud ignore file
├── utils/                   # Utility modules
│   ├── __init__.py
│   ├── document_processor.py  # Document handling
│   ├── storage.py             # GCS operations
│   ├── gemini_client.py       # Gemini API client
│   └── adk_client.py          # ADK integration
├── models/                  # Data models
│   └── schemas.py           # Pydantic schemas
├── data/                    # Resource files
│   ├── prompts/             # Prompt templates
│   ├── schemas/             # JSON output schemas
│   └── few_shot_examples/   # Example data for model training
├── tests/                   # Test files
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

## 🆕 New Features

### Google Agent Development Kit (ADK) Integration
The CV Optimizer now supports processing with Google's Agent Development Kit (ADK). This allows for more complex and stateful interactions with the LLM. To enable ADK:

1. Set `USE_ADK="true"` in your environment variables
2. Specify the ADK agent location with `ADK_AGENT_LOCATION`
3. Follow the [ADK documentation](https://google.github.io/adk-docs/) to create and configure your agent

### Secret Manager Integration
Prompts, schemas, and few-shot examples can now be stored in Google Cloud Secret Manager instead of files or GCS. This provides better security and management for sensitive prompts and configurations.

To enable Secret Manager:
1. Set `USE_SECRETS_MANAGER="true"` in your environment variables
2. Configure the secret prefixes with `PROMPTS_SECRET_PREFIX`, `SCHEMAS_SECRET_PREFIX`, and `EXAMPLES_SECRET_PREFIX`
3. Create secrets in Secret Manager with the appropriate names:
   - `{PROMPTS_SECRET_PREFIX}system-prompt` - For system prompt
   - `{PROMPTS_SECRET_PREFIX}{task}-user-prompt` - For task-specific user prompts
   - `{SCHEMAS_SECRET_PREFIX}{task}-schema` - For task-specific schemas
   - `{EXAMPLES_SECRET_PREFIX}{task}-examples` - For task-specific few-shot examples

### Supabase Authentication
The API now requires JWT authentication through Supabase. This secures the API and allows for user-specific processing and data isolation.

### File Upload Support
The API now accepts direct file uploads via `multipart/form-data` instead of requiring CV documents to be accessible via URL. This simplifies integration with frontend applications and improves security.

### Pydantic V2 Support
The codebase has been updated to use Pydantic v2, which provides better performance and additional features for data validation.

### Enhanced Gemini Integration
The Gemini client has been updated to support the latest features of the google-genai library, including:
- Improved error handling
- Better JSON response parsing
- Support for newer models (gemini-2.0-pro-001, gemini-2.0-flash-001)

## 📦 Deployment

### Environment Variables
See `.env.template` for all required and optional environment variables. The following variables are required for deployment:

- `PROJECT_ID` - Your Google Cloud Project ID
- `GCS_BUCKET_NAME` - Your Google Cloud Storage bucket
- `SUPABASE_JWT_SECRET` - Your Supabase JWT secret
- `SUPABASE_PROJECT_REF` - Your Supabase project reference

### Deploying as a GCP Function
Deploy with sufficient memory and timeout for LLM operations:

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

For PowerShell, use this single-line command:
```powershell
gcloud functions deploy cv_optimizer --gen2 --runtime=python311 --region=europe-west2 --source=. --entry-point=cv_optimizer --trigger-http --memory=2048MB --timeout=540s --set-env-vars="USE_ADK=true,ADK_AGENT_LOCATION=projects/hireable-places/locations/europe-west2/agents/cv-optimizer-agent" --allow-unauthenticated
```

## 🔄 Migration Guide
If migrating from a previous version, follow these steps:

1. Update dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Update your environment variables:
   - Add Supabase authentication variables
   - Configure ADK and Secret Manager settings if needed

3. Update client code to:
   - Send `multipart/form-data` requests with file uploads
   - Include Supabase JWT authentication headers
   - Handle the new response format

4. If using ADK or Secret Manager, configure the respective resources in Google Cloud 