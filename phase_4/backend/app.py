# Vercel entry point for FastAPI application
import sys
import os
import logging

# Set up basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    # Add the src directory to the path so imports work correctly
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

    # Set default environment variables for Vercel if not present
    if not os.getenv("SECRET_KEY"):
        os.environ["SECRET_KEY"] = "fallback-vercel-secret-key-change-in-production-please-make-it-at-least-32-chars-long"
    if not os.getenv("DATABASE_URL"):
        os.environ["DATABASE_URL"] = "sqlite:///./vercel_fallback.db"
    if not os.getenv("BETTER_AUTH_SECRET"):
        os.environ["BETTER_AUTH_SECRET"] = "fallback-better-auth-secret-change-in-production"

    # Ensure VERCEL environment detection
    os.environ["VERCEL_ENV"] = os.environ.get("VERCEL_ENV", "development")
    os.environ["VERCEL"] = os.environ.get("VERCEL", "1")
    os.environ["DEBUG"] = os.environ.get("DEBUG", "false")

    # Import the environment validator but handle it gracefully
    try:
        from src.utils.env_validator import validate_environment
        validate_environment()
    except Exception as e:
        logger.warning(f"Environment validation failed: {e}. Using fallback values.")
        # Set fallback values if validation fails
        os.environ.setdefault("SECRET_KEY", "fallback-vercel-secret-key-change-in-production-please-make-it-at-least-32-chars-long")
        os.environ.setdefault("DATABASE_URL", "sqlite:///./vercel_fallback.db")
        os.environ.setdefault("BETTER_AUTH_SECRET", "fallback-better-auth-secret-change-in-production")

    # Import the FastAPI app from the main module with error handling
    from src.api.main import app

    logger.info("FastAPI app imported successfully")

except ImportError as e:
    logger.error(f"Import error: {e}")
    # Create a minimal app as fallback
    from fastapi import FastAPI

    app = FastAPI(title="Minimal API Fallback", description="Fallback API for Vercel deployment")

    @app.get("/")
    def read_root():
        return {
            "message": "API is running but had import issues",
            "status": "degraded",
            "error": str(e) if 'e' in locals() else "Unknown import error"
        }

    @app.get("/health")
    def health_check():
        return {"status": "degraded", "message": "Running in fallback mode"}

except Exception as e:
    logger.error(f"Unexpected error during app initialization: {e}")
    # Create a minimal app as fallback
    from fastapi import FastAPI

    app = FastAPI(title="Minimal API Fallback", description="Fallback API for Vercel deployment")

    @app.get("/")
    def read_root():
        return {
            "message": "API is running but had initialization issues",
            "status": "error",
            "error": str(e)
        }

    @app.get("/health")
    def health_check():
        return {"status": "error", "message": "App failed to initialize properly"}

# This ensures that Vercel can find the FastAPI application
# Vercel looks for a variable called 'app' in the module