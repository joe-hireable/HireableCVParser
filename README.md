# CV Optimizer Cloud Function

A Google Cloud Function that uses Gemini 2.0 Flash to analyze, optimize, and provide insights for CVs (resumes) based on job descriptions.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
  - [Local Development](#local-development)
  - [Deployment](#deployment)
- [API Usage](#api-usage)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [How It Works](#how-it-works)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

## 🔍 Overview

This cloud function serves as an API for CV (resume) optimization and analysis using Google's Gemini 2.0 Flash Lite AI model. It can parse CVs, analyze them against job descriptions, and provide actionable feedback and optimization suggestions.

## ✨ Features

- **CV Parsing**: Extract structured data from CV documents (PDF or DOCX)
- **Personal Statement Analysis**: Review and improve personal statements/profiles
- **Key Achievements Analysis**: Analyze and enhance key achievements
- **Core Skills Analysis**: Identify and optimize core skills sections
- **Role Analysis**: Evaluate role descriptions and experience
- **CV Scoring**: Score CVs against job descriptions for compatibility
- **OpenTelemetry Integration**: Built-in tracing and monitoring
- **Caching System**: Efficient document caching for improved performance
- **Security Features**: URL validation and domain allowlisting
- **Structured Logging**: JSON-formatted logs for better debugging

## 📋 Prerequisites

- Python 3.11 or higher
- Google Cloud Platform account with billing enabled
- Gemini API access (via Google Cloud AI Platform)
- Google Cloud SDK installed (for deployment)
- Basic understanding of:
  - Python programming
  - REST APIs
  - Google Cloud Platform
  - Git version control

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

4. **Set up Google Cloud credentials**
   - Create a service account in Google Cloud Console
   - Download the JSON key file
   - Set the environment variable:
     ```bash
     # On Windows (PowerShell)
     $env:GOOGLE_APPLICATION_CREDENTIALS="path/to/your/credentials.json"

     # On macOS/Linux
     export GOOGLE_APPLICATION_CREDENTIALS="path/to/your/credentials.json"
     ```

5. **Configure the project**
   - Copy `config.py.example` to `config.py` (if available)
   - Update the following settings in `config.py`:
     - `PROJECT_ID`: Your Google Cloud project ID
     - `GCS_BUCKET_NAME`: Your Google Cloud Storage bucket name
     - `ALLOWED_DOMAINS`: Add any additional domains you need to access

6. **Start the function locally**
   ```bash
   functions-framework --target=cv_optimizer
   ```

7. **Test the function**
   - The function will be available at http://localhost:8080
   - Use tools like Postman or cURL to send requests
   - Example test request:
     ```bash
     curl -X POST http://localhost:8080 \
       -H "Content-Type: application/json" \
       -d '{
         "cv_url": "https://example.com/cv.pdf",
         "task": "parsing"
       }'
     ```

### Deployment

1. **Configure Google Cloud SDK**
   ```bash
   gcloud auth login
   gcloud config set project YOUR_PROJECT_ID
   ```

2. **Deploy the function**
   ```bash
   gcloud functions deploy cv_optimizer \
     --gen2 \
     --runtime=python311 \
     --region=europe-west2 \
     --source=. \
     --entry-point=cv_optimizer \
     --trigger-http \
     --allow-unauthenticated
   ```

3. **Verify deployment**
   - The function URL will be provided in the deployment output
   - Test the deployed function using the same curl command as above

## 📡 API Usage

### Endpoint

`POST https://YOUR_FUNCTION_URL`

### Request Format

```json
{
  "cv_url": "https://example.com/path/to/cv.pdf",
  "jd_url": "https://example.com/path/to/job_description.pdf",
  "task": "parsing|ps|cs|ka|role|scoring",
  "section": "optional_section_name"
}
```

### Task Types

- `parsing`: Extract structured data from a CV
- `ps`: Analyze and optimize Personal Statement
- `cs`: Analyze and optimize Core Skills
- `ka`: Analyze and optimize Key Achievements
- `role`: Analyze and optimize Role descriptions
- `scoring`: Score CV against job description

### Response Format

```json
{
  "status": "success|error|partial",
  "errors": [
    {
      "code": "error_code",
      "message": "Human readable message",
      "field": "field_name",
      "severity": "error|warning"
    }
  ],
  "data": {
    // Task-specific output data
  }
}
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
│   └── gemini_client.py       # Gemini API client
├── prompts/                 # Prompt templates
│   ├── system_prompt.md     # System instructions
│   ├── parsing_user_prompt.md
│   ├── ps_user_prompt.md    # Personal Statement prompts
│   ├── cs_user_prompt.md    # Core Skills prompts
│   ├── ka_user_prompt.md    # Key Achievements prompts
│   └── role_user_prompt.md  # Role analysis prompts
├── schemas/                 # JSON output schemas
│   ├── parsing_schema.json
│   ├── ps_schema.json
│   ├── cs_schema.json
│   ├── ka_schema.json
│   └── role_schema.json
├── few_shot_examples/       # Example data for model training
├── tests/                   # Test files
├── deploy/                  # Deployment scripts
└── docs/                    # Documentation
```

## ⚙️ Configuration

Key configuration settings in `config.py`:

- **GCS_BUCKET_NAME**: Google Cloud Storage bucket for storing documents
- **CV_FOLDER**: Folder for storing CVs in GCS
- **JD_FOLDER**: Folder for storing Job Descriptions in GCS
- **PROJECT_ID**: Google Cloud Project ID
- **LOCATION**: Google Cloud region (default: europe-west9)
- **MODEL_NAME**: Gemini model version to use
- **VERTEX_AI_ENABLED**: Whether to use Vertex AI (or direct Gemini API)
- **ALLOWED_TASKS**: List of valid task types
- **ALLOWED_DOMAINS**: List of trusted domains for URL validation
- **CACHE_TTL_DAYS**: Number of days to keep documents in cache
- **ALLOWED_CONTENT_TYPES**: Supported document types (PDF, DOCX)

## 🛠️ How It Works

1. **Document Processing**:
   - The function receives URLs to CV and job description documents
   - `DocumentProcessor` downloads and extracts text from these documents
   - Documents are stored in Google Cloud Storage for reference
   - Caching system prevents redundant downloads

2. **AI Processing**:
   - Based on the requested task, the function loads appropriate prompts and schemas
   - Text is processed by the Gemini AI model with few-shot examples
   - The response is structured according to the corresponding JSON schema
   - OpenTelemetry traces the entire process for monitoring

3. **Response**:
   - The structured data is returned to the client as a JSON response
   - All responses follow a consistent format with status, errors, and data fields
   - Errors are properly categorized and include helpful messages

## 🔧 Troubleshooting

### Common Issues

1. **Missing Credentials**:
   - Ensure GOOGLE_APPLICATION_CREDENTIALS is set correctly
   - Verify the service account has necessary permissions:
     - Gemini API access
     - Google Cloud Storage access
     - Cloud Functions access (for deployment)

2. **Deployment Failures**:
   - Check that all dependencies are properly listed in requirements.txt
   - Ensure all required directories are included in the deployment
   - Verify your Google Cloud project has billing enabled

3. **Runtime Errors**:
   - Check Cloud Function logs through Google Cloud Console
   - Verify resource files (prompts, schemas, examples) are properly formatted
   - Check OpenTelemetry traces for detailed execution flow

4. **URL Validation Errors**:
   - Ensure URLs are from allowed domains
   - Check if the URLs are accessible
   - Verify the content type is supported (PDF or DOCX)

## 👥 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

### Development Guidelines

- Follow PEP 8 style guide
- Add docstrings to all functions and classes
- Include unit tests for new features
- Update documentation as needed
- Keep commits focused and atomic

### Testing

Before submitting a pull request:
1. Run the test suite: `python -m pytest tests/`
2. Test the function locally
3. Ensure all linting checks pass
4. Update the README if needed 