# Vercel entry point for FastAPI application
# Crash-resistant version with comprehensive error handling
import sys
import os
import logging
import traceback

# Set up basic logging with more detailed configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Add the src directory to the path so imports work correctly
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Set default environment variables for Vercel if not present
# Ensure all secrets are at least 32 characters for security
if not os.getenv("SECRET_KEY"):
    os.environ["SECRET_KEY"] = "fallback-vercel-secret-key-at-least-32-chars-long-please-change-in-production"
if not os.getenv("DATABASE_URL"):
    os.environ["DATABASE_URL"] = "sqlite:///./vercel_fallback.db"
if not os.getenv("BETTER_AUTH_SECRET"):
    os.environ["BETTER_AUTH_SECRET"] = "fallback-better-auth-secret-at-least-32-chars-long-please-change-in-production"

# Ensure VERCEL environment detection
os.environ["VERCEL_ENV"] = os.environ.get("VERCEL_ENV", "development")
os.environ["VERCEL"] = os.environ.get("VERCEL", "1")
os.environ["DEBUG"] = os.environ.get("DEBUG", "false").lower()

def create_fallback_app():
    """Create a minimal FastAPI app that always works as a fallback."""
    from fastapi import FastAPI

    app = FastAPI(
        title="AI-Powered Todo Chatbot API - Fallback Mode",
        description="Minimal API running in fallback mode due to initialization issues",
        version="1.0.0"
    )

    @app.get("/")
    def read_root():
        return {
            "message": "API is running in fallback mode",
            "status": "degraded",
            "environment": os.getenv("VERCEL_ENV", "unknown"),
            "vercel": os.getenv("VERCEL", "unknown")
        }

    @app.get("/health")
    def health_check():
        return {
            "status": "degraded",
            "mode": "fallback",
            "timestamp": __import__('datetime').datetime.utcnow().isoformat()
        }

    @app.get("/debug/info")
    def debug_info():
        return {
            "environment_vars": {
                "VERCEL": os.getenv("VERCEL"),
                "VERCEL_ENV": os.getenv("VERCEL_ENV"),
                "DEBUG": os.getenv("DEBUG"),
                "has_secret_key": bool(os.getenv("SECRET_KEY")),
                "has_database_url": bool(os.getenv("DATABASE_URL")),
                "has_better_auth_secret": bool(os.getenv("BETTER_AUTH_SECRET"))
            },
            "python_version": sys.version,
            "working_directory": os.getcwd(),
            "files_in_dir": os.listdir('.')
        }

    return app

# Initialize the app with comprehensive error handling
try:
    logger.info("Starting FastAPI app initialization...")

    # Validate critical environment variables before importing
    required_vars = ["SECRET_KEY", "DATABASE_URL"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]

    if missing_vars:
        logger.warning(f"Missing required environment variables: {missing_vars}")
        # Still try to continue with fallback values that were set above

    # Attempt to import the main application
    try:
        from src.api.main import app
        logger.info("Successfully imported main FastAPI application")
    except ImportError as e:
        logger.error(f"Failed to import main application: {e}")
        logger.error(f"Traceback: {traceback.format_exc()}")

        # Try alternative import paths
        import sys
        import os
        sys.path.insert(0, os.path.abspath('.'))
        sys.path.insert(0, os.path.abspath('./src'))

        try:
            # Try to import directly from the main module
            import importlib.util
            spec = importlib.util.spec_from_file_location("main", "./src/api/main.py")
            main_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(main_module)
            app = main_module.app
            logger.info("Successfully imported app using importlib")
        except Exception as e2:
            logger.error(f"Alternative import also failed: {e2}")
            app = create_fallback_app()

    except Exception as e:
        logger.error(f"Unexpected error during main import: {e}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        app = create_fallback_app()

    # Add a final health check endpoint to the main app
    @app.get("/crash_health")
    def crash_health_check():
        return {
            "status": "operational",
            "mode": "normal" if 'src.api.main' in sys.modules else "fallback",
            "timestamp": __import__('datetime').datetime.utcnow().isoformat(),
            "has_required_modules": {
                "fastapi": "fastapi" in sys.modules,
                "sqlmodel": "sqlmodel" in sys.modules,
                "pydantic": "pydantic" in sys.modules
            }
        }

    logger.info("FastAPI app initialization completed successfully")

except Exception as e:
    logger.error(f"Critical error during app setup: {e}")
    logger.error(f"Full traceback: {traceback.format_exc()}")
    app = create_fallback_app()

# This ensures that Vercel can find the FastAPI application
# Vercel looks for a variable called 'app' in the module
logger.info("App ready for Vercel deployment")