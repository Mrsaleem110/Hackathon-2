from sqlmodel import Session, create_engine
from contextlib import contextmanager
import os

# Import the get_engine function from the connection module to maintain consistency
from .connection import get_engine

@contextmanager
def get_session():
    """Provide a transactional scope around a series of operations."""
    engine = get_engine()
    with Session(engine) as session:
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()