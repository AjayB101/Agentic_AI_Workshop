import os
from pathlib import Path

# Database Configuration
CHROMA_DB_PATH = "./chroma_db"
COLLECTION_NAME = "student_placement_data"

# API Keys (Use environment variables in production)
# Replace with your actual key
GOOGLE_API_KEY = "AIzaSyDFBvIZVRQ1Mc15jLsdyY6m2fNq9BuNPII"
HUGGINGFACE_API_TOKEN = os.getenv(
    "HUGGINGFACE_API_TOKEN", "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")

# Model Configuration
DEFAULT_MODEL = "gemini-1.5-flash"
TEMPERATURE = 0.3
MAX_TOKENS = 512

# Scoring Weights
ACADEMIC_WEIGHTS = {
    "attendance": 0.3,
    "test_score": 0.3,
    "assignment_percentage": 0.3,
    "event_participation_bonus": 10
}

READINESS_WEIGHTS = {
    "technical": 0.6,
    "communication": 0.4
}

# Thresholds
PERFORMANCE_THRESHOLDS = {
    "excellent": 80,
    "good": 70,
    "needs_improvement": 60
}

# File Upload Settings
ALLOWED_FILE_TYPES = ["csv"]
MAX_FILE_SIZE_MB = 10

# UI Configuration
PAGE_TITLE = "🎓 AI-Powered Placement Readiness System"
PAGE_ICON = "🎓"

# Logging Configuration
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
