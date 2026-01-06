from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"
        # Allow extra fields to prevent validation errors in serverless environments
        extra = "ignore"
        # Allow validation to be skipped in some cases
        validate_assignment = False


def get_settings():
    """Lazy load settings to avoid import-time validation errors in serverless environments"""
    try:
        return Settings()
    except Exception as e:
        # If settings validation fails (e.g., missing env vars), provide defaults for serverless
        # This allows the app to start even if environment variables aren't available at import time
        print(f"Warning: Could not load settings from environment: {e}")
        return Settings(
            DATABASE_URL=os.getenv("DATABASE_URL", "sqlite:///./test.db"),
            SECRET_KEY=os.getenv("SECRET_KEY", "fallback-secret-key-for-serverless")
        )


# Avoid creating settings instance at module import time in serverless environments
# Use the get_settings() function instead to create settings when needed
settings = None