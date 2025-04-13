"""Configuration settings for the CV Optimizer Cloud Function.
This module defines all configuration parameters used throughout the application.
All sensitive values should be loaded from environment variables.
"""
import os
from typing import List, Dict, Any

# Google Cloud Storage settings
GCS_BUCKET_NAME = os.getenv("GCS_BUCKET_NAME", "gcp-parser")
CV_FOLDER = "cvs"
JD_FOLDER = "jds"

# Project settings - Load from environment with fallbacks
PROJECT_ID = os.getenv("PROJECT_ID", "hireable-places")
LOCATION = os.getenv("LOCATION", "europe-west9")

# Vertex AI settings
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "gemini-pro")
SUPPORTED_MODELS: List[str] = [
    "gemini-pro",
    "gemini-pro-vision",
    "gemini-1.5-pro",
]
VERTEX_AI_ENABLED = os.getenv("VERTEX_AI_ENABLED", "true").lower() in ("true", "1", "yes")

# Model configuration
DEFAULT_GENERATION_CONFIG: Dict[str, Any] = {
    "temperature": float(os.getenv("MODEL_TEMPERATURE", "0.5")),
    "top_p": float(os.getenv("MODEL_TOP_P", "0.95")),
    "top_k": int(os.getenv("MODEL_TOP_K", "40")),
    "max_output_tokens": int(os.getenv("MODEL_MAX_OUTPUT_TOKENS", "8192")),
    "candidate_count": int(os.getenv("MODEL_CANDIDATE_COUNT", "1"))
}

# Google ADK settings
USE_ADK = os.getenv("USE_ADK", "false").lower() in ("true", "1", "yes")
ADK_AGENT_LOCATION = os.getenv(
    "ADK_AGENT_LOCATION",
    f"projects/{PROJECT_ID}/locations/{LOCATION}/agents/cv-optimizer-agent"
)

# Secret Manager settings
SECRET_MANAGER_PROJECT = PROJECT_ID
SECRET_MANAGER_LOCATION = LOCATION
PROMPTS_SECRET_PREFIX = os.getenv("PROMPTS_SECRET_PREFIX", "cv-optimizer-prompt-")
SCHEMAS_SECRET_PREFIX = os.getenv("SCHEMAS_SECRET_PREFIX", "cv-optimizer-schema-")
EXAMPLES_SECRET_PREFIX = os.getenv("EXAMPLES_SECRET_PREFIX", "cv-optimizer-examples-")
USE_SECRETS_MANAGER = os.getenv("USE_SECRETS_MANAGER", "false").lower() in ("true", "1", "yes")

# File paths (used when not using Secret Manager)
PROMPTS_DIR = "prompts"
SCHEMAS_DIR = "schemas"
FEW_SHOT_EXAMPLES_DIR = "few_shot_examples"

# Task validation
ALLOWED_TASKS: List[str] = ["parsing", "ps", "cs", "ka", "role", "scoring"]

# Logging configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Cache configuration
CACHE_TTL_DAYS = int(os.getenv("CACHE_TTL_DAYS", "30"))
MEMORY_CACHE_SIZE = int(os.getenv("MEMORY_CACHE_SIZE", "100"))
CACHE_COMPRESSION_THRESHOLD = int(os.getenv("CACHE_COMPRESSION_THRESHOLD", "1000000"))

# Content type validation
ALLOWED_CONTENT_TYPES: List[str] = [
    'application/pdf',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
]

# Retry configuration for Vertex AI
MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))
BASE_DELAY = int(os.getenv("BASE_DELAY", "1"))
MAX_DELAY = int(os.getenv("MAX_DELAY", "10")) 