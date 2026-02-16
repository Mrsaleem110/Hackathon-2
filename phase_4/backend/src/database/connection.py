from sqlmodel import create_engine, Session
from typing import Generator
import os

# Database URL from environment - use NeonDB as required
NEON_DATABASE_URL = os.getenv("NEON_DATABASE_URL")
DATABASE_URL = NEON_DATABASE_URL or os.getenv("DATABASE_URL", "sqlite:///./todo_chatbot_local.db")

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
    # In serverless, we want to avoid connection pooling issues
    connect_args = {}
    if DATABASE_URL.startswith("postgresql"):
        connect_args = {
            "pool_pre_ping": True,
            "pool_recycle": 300,
            "pool_size": 1,
            "max_overflow": 0,
        }
        # Only add sslmode=require if it's a Neon DB connection
        if NEON_DATABASE_URL or "neon.tech" in DATABASE_URL:
            connect_args["connect_args"] = {"sslmode": "require"}

    return create_engine(DATABASE_URL, echo=False, **connect_args)

def get_session() -> Generator[Session, None, None]:
    engine = get_engine()
    with Session(engine) as session:
        yield session