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
    except Exception:
        # If settings validation fails (e.g., missing env vars), provide defaults for serverless
        # This allows the app to start even if environment variables aren't available at import time
        return Settings(
            DATABASE_URL=os.getenv("DATABASE_URL", "sqlite:///./test.db"),
            SECRET_KEY=os.getenv("SECRET_KEY", "fallback-secret-key-for-serverless")
        )


# Create settings instance only when needed to avoid import-time validation
try:
    settings = Settings()
except Exception:
    # In serverless environments where env vars might not be available at import time
    settings = None