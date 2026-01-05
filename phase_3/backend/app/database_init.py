from .database import get_engine
from sqlmodel import SQLModel


def create_db_and_tables():
    """Create database tables"""
    print("Creating database tables...")
    engine = get_engine()
    SQLModel.metadata.create_all(bind=engine)
    print("Database tables created successfully!")


if __name__ == "__main__":
    create_db_and_tables()