
import os
import sys

# Add backend directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.gemini_client import gemini_client
from app.config import get_settings

def test_gemini_connection():
    settings = get_settings()
    if not settings.GEMINI_API_KEY:
        print("❌ GEMINI_API_KEY is not set in .env file.")
        print("Please add your Gemini API key to backend/.env")
        return

    print(f"Checking configuration for model: {settings.GEMINI_MODEL}...")
    
    try:
        response = gemini_client.generate_content("Hello! Are you working?")
        print(f"✅ Gemini API Connection Successful!")
        print(f"Response: {response}")
    except Exception as e:
        print(f"❌ Gemini API Error: {str(e)}")

if __name__ == "__main__":
    test_gemini_connection()
