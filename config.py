"""Configuration settings for the CV Optimizer Cloud Function."""
import os

# Google Cloud Storage settings
GCS_BUCKET_NAME = "gcp-parser"
CV_FOLDER = "cvs"
JD_FOLDER = "jds"

# Project settings
PROJECT_ID = "hireable-places"
LOCATION = "europe-west9"  # Paris region

# Gemini API settings
DEFAULT_MODEL = "gemini-2.5-pro-preview-03-25"
SUPPORTED_MODELS = [
    "gemini-2.5-pro-preview-03-25",     # Default model
    "gemini-2.0-flash", # Faster model
    "gemini-2.5-flash-lite"        # Added higher quality model
]
VERTEX_AI_ENABLED = True  # Flag to switch between direct Gemini API and Vertex AI

# Google ADK settings
USE_ADK = os.environ.get("USE_ADK", "false").lower() in ("true", "1", "yes")
ADK_AGENT_LOCATION = os.environ.get("ADK_AGENT_LOCATION", f"projects/{PROJECT_ID}/locations/{LOCATION}/agents/cv-optimizer-agent")

# Secret Manager settings
SECRET_MANAGER_PROJECT = PROJECT_ID
SECRET_MANAGER_LOCATION = LOCATION
PROMPTS_SECRET_PREFIX = "cv-optimizer-prompt-"
SCHEMAS_SECRET_PREFIX = "cv-optimizer-schema-"
EXAMPLES_SECRET_PREFIX = "cv-optimizer-examples-"
USE_SECRETS_MANAGER = os.environ.get("USE_SECRETS_MANAGER", "false").lower() in ("true", "1", "yes")

# File paths (used when not using Secret Manager)
PROMPTS_DIR = "prompts"
SCHEMAS_DIR = "schemas"
FEW_SHOT_EXAMPLES_DIR = "few_shot_examples"

# Task validation
ALLOWED_TASKS = ["parsing", "ps", "cs", "ka", "role", "scoring"]

# Logging configuration
LOG_LEVEL = "INFO"

# Cache configuration
CACHE_TTL_DAYS = 30  # Number of days to keep documents in cache
MEMORY_CACHE_SIZE = 100  # Maximum number of documents to keep in memory cache
CACHE_COMPRESSION_THRESHOLD = 1000000  # Size in bytes above which to compress cached content (~1MB)

# Content type validation
ALLOWED_CONTENT_TYPES = [
    'application/pdf',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
] 