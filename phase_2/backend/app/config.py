from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    database_url: str = "sqlite:///./todo_app.db"
    secret_key: str = "fallback-secret-key-for-vercel"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    class Config:
        env_file = ".env"
        extra = "ignore"  # Ignore extra fields that might not be in the env


# Initialize settings with fallback values
settings = Settings()