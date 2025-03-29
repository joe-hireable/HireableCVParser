"""Configuration settings for the CV Optimizer Cloud Function."""

# Google Cloud Storage settings
GCS_BUCKET_NAME = "gcp-parser"
CV_FOLDER = "cvs"
JD_FOLDER = "jds"

# Project settings
PROJECT_ID = "hireable-places"
LOCATION = "europe-west9"  # Paris region

# Gemini API settings
DEFAULT_MODEL = "gemini-2.0-flash-001"
SUPPORTED_MODELS = [
    "gemini-2.0-flash-001",     # Default model
    "gemini-2.0-flash-lite-001" # Faster model
]
VERTEX_AI_ENABLED = True  # Flag to switch between direct Gemini API and Vertex AI

# File paths
PROMPTS_DIR = "prompts"
SCHEMAS_DIR = "schemas"
FEW_SHOT_EXAMPLES_DIR = "few_shot_examples"

# Task validation
ALLOWED_TASKS = ["parsing", "ps", "cs", "ka", "role", "scoring"]

# URL validation
ALLOWED_DOMAINS = [
    'storage.googleapis.com',  # Google Cloud Storage
    'example.com',             # Example domain
    'githubusercontent.com',   # GitHub content
    'raw.githubusercontent.com', # GitHub raw content
    'bubble.io',               # Bubble.io main domain
    'bubble-io.s3.amazonaws.com',  # Bubble.io S3 storage
    'bubble-io-files.s3.amazonaws.com',  # Bubble.io file storage
    'bubble-io-files-prod.s3.amazonaws.com',  # Bubble.io production file storage
    'bubble-io-files-staging.s3.amazonaws.com',  # Bubble.io staging file storage
    'hireable-cv-branding.lovable.app', # Added new allowed domain
    'localhost',               # Local development
    '172.30.16.1',             # Local network development
    '192.168.1.113'            # Local network development
]

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