"""Configuration settings for the CV Optimizer Cloud Function."""

# Google Cloud Storage settings
GCS_BUCKET_NAME = "gcp-parser"
CV_FOLDER = "cvs"
JD_FOLDER = "jds"

# Project settings
PROJECT_ID = "hireable-places"
LOCATION = "europe-west9"  # London region

# Gemini API settings
MODEL_NAME = "gemini-2.0-flash"
VERTEX_AI_ENABLED = True  # Flag to switch between direct Gemini API and Vertex AI

# File paths
PROMPTS_DIR = "prompts"
SCHEMAS_DIR = "schemas"
FEW_SHOT_EXAMPLES_DIR = "few_shot_examples"

# Task validation
ALLOWED_TASKS = ["parsing", "ps", "cs", "ka", "role", "scoring"]

# Logging configuration
LOG_LEVEL = "INFO" 