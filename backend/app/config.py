import os
from dotenv import load_dotenv

load_dotenv()

# OpenAI Configuration
# Gemini Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

# Application Settings
APP_NAME = os.getenv("APP_NAME", "Diamond Chatbot")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")

# Excel Data Path
EXCEL_FILE_PATH = os.getenv("EXCEL_FILE_PATH", "data/diamonds.xlsx")


# CORS Settings
cors_env = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://localhost:3000")
CORS_ORIGINS = cors_env.split(",") if cors_env else []
