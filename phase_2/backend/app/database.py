from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from app.config import get_settings

# Import models to ensure they're registered with SQLModel before accessing metadata
from app.models.user import User
from app.models.item import Item
from app.models.session import Session

def get_engine():
    """Create and return database engine, only when settings are available"""
    settings = get_settings()

    if settings.DATABASE_URL.startswith("sqlite"):
        # SQLite specific configuration
        engine = create_engine(
            settings.DATABASE_URL,
            echo=False,  # Set to False in production
            pool_pre_ping=True,
            pool_recycle=300,
        )
    else:
        # PostgreSQL/NeonDB specific configuration
        engine = create_engine(
            settings.DATABASE_URL,
            echo=False,  # Set to False in production
            pool_pre_ping=True,
            pool_recycle=300,
            pool_size=20,
            max_overflow=30,
            pool_timeout=30,
            connect_args={
                "connect_timeout": 10,
            }
        )
    return engine

# Create engine and session factory functions (not objects) to defer initialization
def get_session_local():
    """Get sessionmaker class, only when needed"""
    engine = get_engine()
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Dependency to get database session"""
    SessionLocal = get_session_local()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Base is the metadata object for SQLModel (after models are imported)
Base = SQLModel.metadata