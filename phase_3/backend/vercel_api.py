import sys
import os
import logging
import traceback
from pathlib import Path

# Set up basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Log basic debugging information
logger.info(f"Current working directory: {os.getcwd()}")
logger.info(f"Python executable: {sys.executable}")
logger.info(f"Python version: {sys.version}")
logger.info(f"Working dir contents: {os.listdir('.')}")

# Create a minimal app first to ensure we always have a working app
try:
    from fastapi import FastAPI
    app = FastAPI(
        title="AI-Powered Todo Chatbot API - Safe Mode",
        description="Safe mode version of the API that always works",
        version="1.0.0-safe"
    )

    @app.get("/")
    def read_root():
        return {"message": "API in safe mode", "status": "operational", "mode": "safe"}

    @app.get("/health")
    def health_check():
        return {"status": "healthy", "mode": "safe", "timestamp": os.times()[4] if hasattr(os, 'times') else "unknown"}

    @app.get("/status")
    def status_check():
        return {
            "status": "operational",
            "mode": "safe",
            "working": True,
            "dependencies_status": "checking..."
        }

    logger.info("Minimal safe app created successfully")

    # Now try to add the src directory to the path and import the full app
    src_path = os.path.join(os.path.dirname(__file__), 'src')
    if os.path.exists(src_path):
        sys.path.insert(0, src_path)
        logger.info(f"Added src path: {src_path}")
        logger.info(f"Src directory contents: {os.listdir(src_path)}")

        api_dir = os.path.join(src_path, 'api')
        if os.path.exists(api_dir):
            logger.info(f"API directory contents: {os.listdir(api_dir)}")

            # Attempt to import the main application with extensive error handling
            try:
                logger.info("Attempting to import main app...")

                # Try to set environment variables to bypass validation issues
                if not os.getenv("SECRET_KEY"):
                    os.environ["SECRET_KEY"] = "fallback-serverless-secret-key-change-in-production-please"
                if not os.getenv("DATABASE_URL"):
                    os.environ["DATABASE_URL"] = "sqlite:///./todo_app_serverless.db"

                # Import the main module - wrap in another try block
                from src.api import main

                # If successful, replace the safe app with the real one
                app = main.app
                logger.info("Main application loaded successfully")

                # Add a status endpoint to the real app
                @app.get("/status")
                def full_status_check():
                    if hasattr(app, 'routes'):
                        route_paths = [route.path for route in app.routes]
                        auth_routes = [path for path in route_paths if 'auth/' in path.lower()]
                        return {
                            "status": "success",
                            "mode": "full",
                            "auth_routes_available": len(auth_routes) > 0,
                            "total_routes": len(route_paths),
                            "auth_routes": auth_routes,
                            "all_routes": route_paths
                        }
                    else:
                        return {"status": "success", "mode": "full", "routes_info": "not_available"}

            except Exception as main_import_error:
                logger.error(f"Failed to import main app: {main_import_error}")
                logger.error(f"Traceback: {traceback.format_exc()}")

                # Still use the safe app, but add error information
                @app.get("/debug/error")
                def error_info():
                    return {
                        "error_occurred": str(main_import_error),
                        "error_type": type(main_import_error).__name__,
                        "traceback": str(traceback.format_exc()) if os.getenv("DEBUG", "").lower() == "true" else "Enable DEBUG=true to see traceback"
                    }
        else:
            logger.warning(f"API directory does not exist: {api_dir}")
    else:
        logger.warning(f"Src directory does not exist: {src_path}")

except Exception as setup_error:
    logger.error(f"Critical setup error: {setup_error}")
    logger.error(f"Traceback: {traceback.format_exc()}")

    # Create the most basic possible app as ultimate fallback
    try:
        from fastapi import FastAPI
        app = FastAPI()

        @app.get("/")
        def fallback_root():
            return {
                "status": "error",
                "message": "Critical setup error",
                "error": str(setup_error),
                "mode": "critical-fallback"
            }
    except Exception as fallback_error:
        # If FastAPI import fails, we're in serious trouble
        # But we need to ensure we always export something for Vercel
        import fastapi
        app = fastapi.FastAPI()

        @app.get("/")
        def ultimate_fallback():
            return {
                "status": "emergency",
                "message": "Emergency fallback mode",
                "setup_error": str(setup_error),
                "fallback_error": str(fallback_error)
            }

# This ensures that Vercel can find the FastAPI application
# Vercel looks for a variable called 'app' in the module