from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application configuration settings"""
    
    # OpenAI Configuration
    # Gemini Configuration
    GEMINI_API_KEY: str
    GEMINI_MODEL: str = "Gemini 2.5 Flash-Lite"
    
    # Application Settings
    APP_NAME: str = "Diamond Chatbot"
    APP_VERSION: str = "1.0.0"
    
    # Excel Data Path
    EXCEL_FILE_PATH: str = "data/diamonds.xlsx"
    
    # Chat Configuration
    MAX_CHAT_HISTORY: int = 10
    
    # CORS Settings
    CORS_ORIGINS: list = ["http://localhost:5173", "http://localhost:3000"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()
