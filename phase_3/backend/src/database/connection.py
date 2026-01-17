from sqlmodel import create_engine, Session
from typing import Generator
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database URL from environment - use NeonDB as required
NEON_DB_URL = os.getenv("NEON_DATABASE_URL")
DATABASE_URL = NEON_DB_URL or os.getenv("DATABASE_URL", "sqlite:///./todo_chatbot_local.db")

# If using NeonDB, ensure SSL is properly configured
if "neon.tech" in DATABASE_URL:
    # Ensure the NeonDB URL has proper SSL parameters
    if "?sslmode=" not in DATABASE_URL:
        DATABASE_URL += "?sslmode=require"

# Create engine
engine = create_engine(DATABASE_URL, echo=True)

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session