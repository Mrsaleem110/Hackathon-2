import sys
import os
import logging
import traceback
from pathlib import Path

# Add the src directory to the path so imports work correctly
src_path = os.path.join(os.path.dirname(__file__), 'src')
sys.path.insert(0, src_path)

# Set up basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Log extensive debugging information
logger.info(f"Current working directory: {os.getcwd()}")
logger.info(f"Python executable: {sys.executable}")
logger.info(f"Python version: {sys.version}")
logger.info(f"Python path: {sys.path[:5]}...")  # First 5 entries
logger.info(f"Working dir contents: {os.listdir('.')}")
logger.info(f"Src directory exists: {os.path.exists(src_path)}")
if os.path.exists(src_path):
    logger.info(f"Src directory contents: {os.listdir(src_path)}")
    api_dir = os.path.join(src_path, 'api')
    logger.info(f"API directory exists: {os.path.exists(api_dir)}")
    if os.path.exists(api_dir):
        logger.info(f"API directory contents: {os.listdir(api_dir)}")

# Try to import the app with maximum error reporting
try:
    logger.info("Attempting to import main app...")

    # Try to import specific modules to identify where the issue occurs
    logger.info("About to import from src.api.main")

    # Import the main module
    from src.api import main
    logger.info("Main module imported successfully")

    # Access the app instance
    app = main.app
    logger.info("FastAPI app accessed successfully")

    # Verify app has the expected attributes
    logger.info(f"App object type: {type(app)}")
    if hasattr(app, 'routes'):
        logger.info(f"Number of registered routes: {len(app.routes)}")
        route_paths = [route.path for route in app.routes]
        logger.info(f"All registered routes: {route_paths}")

        # Specifically check for auth routes
        auth_routes = [path for path in route_paths if 'auth/' in path.lower()]
        logger.info(f"Auth-related routes found: {auth_routes}")

        # Add a test route to verify app is working
        @app.get("/status")
        def status_check():
            return {
                "status": "success",
                "auth_routes_available": len(auth_routes) > 0,
                "total_routes": len(route_paths),
                "auth_routes": auth_routes,
                "all_routes": route_paths
            }
    else:
        logger.warning("App object doesn't have 'routes' attribute")


except Exception as e:
    logger.error(f"Unexpected error during app import: {e}")
    logger.error(f"Traceback: {traceback.format_exc()}")

    # Check if this is specifically an environment validation error
    if "environment" in str(e).lower() or "secret_key" in str(e).lower() or "database_url" in str(e).lower():
        logger.info("Detected environment validation error - attempting to patch environment")

        # Set minimal environment variables to allow startup
        if not os.getenv("SECRET_KEY"):
            os.environ["SECRET_KEY"] = "fallback-serverless-secret-key-change-in-production-please"
        if not os.getenv("DATABASE_URL"):
            os.environ["DATABASE_URL"] = "sqlite:///./todo_app_serverless.db"

        # Now try to import again with patched environment
        try:
            from src.api import main
            app = main.app
            logger.info("Successfully imported app after environment patching")
        except Exception as retry_e:
            logger.error(f"Retry import also failed: {retry_e}")
            logger.error(f"Retry traceback: {traceback.format_exc()}")

            # Create a basic fallback app
            from fastapi import FastAPI
            app = FastAPI()

            @app.get("/")
            def read_root():
                return {
                    "status": "error",
                    "message": f"Critical startup error after environment patch: {str(retry_e)}",
                    "original_error": str(e),
                    "cwd": os.getcwd(),
                    "src_exists": os.path.exists(src_path),
                    "api_exists": os.path.exists(os.path.join(src_path, 'api')),
                    "traceback": str(traceback.format_exc())
                }

            @app.get("/status")
            def status_check():
                return {
                    "status": "error",
                    "description": f"Critial startup error: {str(retry_e)}",
                    "original_error": str(e),
                    "traceback": str(traceback.format_exc())
                }
    else:
        # Create a basic fallback app
        from fastapi import FastAPI
        app = FastAPI()

        @app.get("/")
        def read_root():
            return {
                "status": "error",
                "message": f"Unexpected error: {str(e)}",
                "type": type(e).__name__,
                "traceback": str(traceback.format_exc())
            }

        @app.get("/status")
        def status_check():
            return {
                "status": "error",
                "description": f"Unexpected error: {str(e)}",
                "type": type(e).__name__,
                "traceback": str(traceback.format_exc())
            }


# This ensures that Vercel can find the FastAPI application
# Vercel looks for a variable called 'app' in the module