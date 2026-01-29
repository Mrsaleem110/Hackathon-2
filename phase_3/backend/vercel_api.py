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

except ImportError as e:
    logger.error(f"Import error: {e}")
    logger.error(f"Traceback: {traceback.format_exc()}")

    # Log specific details about the import issue
    import sys
    logger.error(f"Sys path: {sys.path}")

    # Check if src.api.main exists
    main_module_path = os.path.join(src_path, 'api', 'main.py')
    logger.error(f"Main module path exists: {os.path.exists(main_module_path)}")

    if os.path.exists(main_module_path):
        logger.error(f"Main module size: {os.path.getsize(main_module_path)} bytes")
        try:
            with open(main_module_path, 'r', encoding='utf-8') as f:
                content = f.read(500)  # Read first 500 chars to check for syntax issues
                logger.error(f"Start of main.py: {repr(content)}")
        except Exception as read_err:
            logger.error(f"Could not read main.py: {read_err}")

    # Create a basic fallback app
    from fastapi import FastAPI
    app = FastAPI()

    @app.get("/")
    def read_root():
        return {
            "status": "error",
            "message": f"Failed to import main app: {str(e)}",
            "cwd": os.getcwd(),
            "src_exists": os.path.exists(src_path),
            "api_exists": os.path.exists(os.path.join(src_path, 'api')),
            "main_py_exists": os.path.exists(main_module_path),
            "traceback": str(traceback.format_exc())
        }

    @app.get("/status")
    def status_check():
        return {
            "status": "error",
            "description": f"Import failed: {str(e)}",
            "traceback": str(traceback.format_exc())
        }

except AttributeError as e:
    logger.error(f"Attribute error during import: {e}")
    logger.error(f"Traceback: {traceback.format_exc()}")

    # Create a basic fallback app
    from fastapi import FastAPI
    app = FastAPI()

    @app.get("/")
    def read_root():
        return {
            "status": "error",
            "message": f"Attribute error: {str(e)}",
            "details": "There might be an issue with the main.py file structure",
            "traceback": str(traceback.format_exc())
        }

    @app.get("/status")
    def status_check():
        return {
            "status": "error",
            "description": f"Attribute error: {str(e)}",
            "traceback": str(traceback.format_exc())
        }

except Exception as e:
    logger.error(f"Unexpected error during app import: {e}")
    logger.error(f"Traceback: {traceback.format_exc()}")

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