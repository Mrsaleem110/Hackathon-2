from .database import engine, Base


def create_db_and_tables():
    """Create database tables"""
    print("Creating database tables...")
    Base.create_all(bind=engine)
    print("Database tables created successfully!")


if __name__ == "__main__":
    create_db_and_tables()