from sqlmodel import create_engine, Session
from typing import Generator
import os

# Database URL from environment - use NeonDB as required
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo_chatbot_local.db")

# If using NeonDB, ensure SSL is properly configured
if DATABASE_URL and "neon.tech" in DATABASE_URL:
    # Ensure the NeonDB URL has proper SSL parameters
    if "?sslmode=" not in DATABASE_URL:
        if "?" in DATABASE_URL:
            DATABASE_URL += "&sslmode=require"
        else:
            DATABASE_URL += "?sslmode=require"

# Create engine with serverless-friendly settings
def get_engine():
    """Create database engine with appropriate settings for serverless environment"""
    engine_kwargs = {
        "echo": False
    }

    # In serverless, we want to avoid connection pooling issues
    if DATABASE_URL.startswith("postgresql"):
        engine_kwargs["pool_pre_ping"] = True
        engine_kwargs["pool_recycle"] = 300
        engine_kwargs["pool_size"] = 1
        engine_kwargs["max_overflow"] = 0
        engine_kwargs["connect_args"] = {
            "sslmode": "require"
        }

    return create_engine(DATABASE_URL, **engine_kwargs)

def get_session() -> Generator[Session, None, None]:
    engine = get_engine()
    with Session(engine) as session:
        yield session