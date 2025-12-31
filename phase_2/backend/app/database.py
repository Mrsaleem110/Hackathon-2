from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from app.config import settings

# Import models to ensure they're registered with SQLModel before accessing metadata
from app.models.user import User
from app.models.item import Item
from app.models.session import Session

# Create the database engine
if settings.database_url.startswith("sqlite"):
    # SQLite specific configuration
    engine = create_engine(
        settings.database_url,
        echo=False,  # Set to False in production
        pool_pre_ping=True,
        pool_recycle=300,
    )
else:
    # PostgreSQL/NeonDB specific configuration
    engine = create_engine(
        settings.database_url,
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

# Create a configured "SessionLocal" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Base is the metadata object for SQLModel (after models are imported)
Base = SQLModel.metadata