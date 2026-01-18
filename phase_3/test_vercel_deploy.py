#!/usr/bin/env python3
"""
Test script to verify the application can be imported without errors
This simulates the Vercel import process to catch potential issues
"""

import sys
import os
import traceback

# Add the backend src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend', 'src'))

def test_imports():
    """Test importing the main application components"""
    print("Testing application imports...")

    try:
        # Test importing the Vercel entry point
        print("1. Testing vercel_api.py import...")
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
        import vercel_api
        print("   [OK] vercel_api.py imported successfully")

        # Test that the app object exists
        if hasattr(vercel_api, 'app'):
            print("   [OK] App object found in vercel_api")
        else:
            print("   [ERROR] App object not found in vercel_api")
            return False

        # Test importing the main module directly
        print("2. Testing src.api.main import...")
        from src.api.main import app
        print("   [OK] src.api.main imported successfully")

        # Test database connection
        print("3. Testing database connection...")
        from src.database.connection import get_engine, get_session
        print("   [OK] Database connection imports successful")

        # Test models
        print("4. Testing model imports...")
        from src.models.user import User
        from src.models.task import Task
        print("   [OK] Model imports successful")

        print("\n[SUCCESS] All imports successful! Application should work on Vercel.")
        return True

    except ImportError as e:
        print(f"   [ERROR] Import error: {e}")
        print("   Full traceback:")
        traceback.print_exc()
        return False
    except Exception as e:
        print(f"   [ERROR] Unexpected error: {e}")
        print("   Full traceback:")
        traceback.print_exc()
        return False

def test_environment_vars():
    """Test that required environment variables are available"""
    print("\nTesting environment variables...")

    required_vars = ['DATABASE_URL']
    missing_vars = []

    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)

    if missing_vars:
        print(f"   [WARN] Missing environment variables: {missing_vars}")
        print("   Note: This is expected in local testing but critical for Vercel deployment")
    else:
        print("   [OK] All required environment variables are set")

    return True

if __name__ == "__main__":
    print("Vercel Deployment Test Script")
    print("=" * 40)

    imports_ok = test_imports()
    env_ok = test_environment_vars()

    print("\n" + "=" * 40)
    if imports_ok:
        print("[SUCCESS] Application import test PASSED")
        print("[SUCCESS] Ready for Vercel deployment")
    else:
        print("[ERROR] Application import test FAILED")
        print("[ERROR] Fix the above issues before deploying to Vercel")
        sys.exit(1)