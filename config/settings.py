import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:7999")
API_TIMEOUT = int(os.getenv("API_TIMEOUT", 30))

# Authentication
API_TOKEN = os.getenv("API_TOKEN", "")
API_KEY = os.getenv("API_KEY", "")

# Teacher Credentials
TEACHER_EMAIL = os.getenv("TEACHER_EMAIL", "teacher@example.com")
TEACHER_PASSWORD = os.getenv("TEACHER_PASSWORD", "password123")
TEACHER_NAME = os.getenv("TEACHER_NAME", "Teacher")

# Environment
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
DEBUG = os.getenv("DEBUG", "True").lower() == "true"

# Headers padrão
DEFAULT_HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": "API-Tests/1.0",
}

if API_TOKEN:
    DEFAULT_HEADERS["Authorization"] = f"Bearer {API_TOKEN}"
