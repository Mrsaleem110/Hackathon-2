#!/usr/bin/env python3
"""
Test script to verify Neon database connection
"""
import os
import sys
from sqlmodel import select
from backend.src.database.connection import get_engine, get_session
from backend.src.models.user import User  # Adjust import based on your actual models

def test_neon_connection():
    print("Testing Neon database connection...")

    # Check if NEON_DATABASE_URL is set
    neon_url = os.getenv("NEON_DATABASE_URL")
    db_url = os.getenv("DATABASE_URL")

    print(f"NEON_DATABASE_URL: {'SET' if neon_url else 'NOT SET'}")
    print(f"DATABASE_URL: {'SET' if db_url else 'NOT SET'}")

    if neon_url:
        print(f"Using Neon database: {neon_url.replace(neon_url.split(':')[2], ':***@***').replace(neon_url.split('@')[1].split('/')[0], '***.neon.tech')}")
    else:
        print("No Neon database URL found, will use fallback database")

    try:
        # Create engine and test connection
        engine = get_engine()

        # Test basic connection
        with engine.connect() as conn:
            result = conn.execute(select([1]))
            print("✓ Database connection successful!")

        # Test session creation
        with get_session() as session:
            print("✓ Session creation successful!")

        print("\nNeon database connection test completed successfully!")
        return True

    except Exception as e:
        print(f"✗ Database connection failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_neon_connection()
    sys.exit(0 if success else 1)