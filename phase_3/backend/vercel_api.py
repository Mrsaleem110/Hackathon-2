import sys
import os
import logging
import traceback

# Add the src directory to the path so imports work correctly
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Set up basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Log the current working directory and Python path for debugging
logger.info(f"Current working directory: {os.getcwd()}")
logger.info(f"Python path: {sys.path}")
logger.info(f"Files in src directory: {os.listdir(os.path.join(os.path.dirname(__file__), 'src')) if os.path.exists(os.path.join(os.path.dirname(__file__), 'src')) else 'src dir not found'}")

# Create a basic fallback app first, so we have something that works even if imports fail
from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Fallback app running", "status": "basic functionality available"}

@app.get("/status")
def status_check():
    return {"status": "reachable", "description": "The server is reachable but may have import issues"}

try:
    # Import the FastAPI app from the main module
    from src.api.main import app
    logger.info("FastAPI app imported successfully")
    logger.info("App object created, checking if routes are registered...")

    # Log registered routes for debugging
    if hasattr(app, 'routes'):
        route_paths = [route.path for route in app.routes]
        logger.info(f"Registered routes: {route_paths}")

        # Specifically check for auth routes
        auth_routes = [path for path in route_paths if 'auth' in path.lower()]
        logger.info(f"Auth-related routes: {auth_routes}")

except ImportError as e:
    logger.error(f"Import error: {e}")
    logger.error(f"Traceback: {traceback.format_exc()}")

    # The app variable is already defined as a fallback, so we'll add error routes to it
    @app.get("/error-details")
    def error_details():
        return {"error": f"Failed to import main app: {str(e)}", "traceback": traceback.format_exc()}

except Exception as e:
    logger.error(f"Unexpected error during app import: {e}")
    logger.error(f"Traceback: {traceback.format_exc()}")

    # The app variable is already defined as a fallback, so we'll add error routes to it
    @app.get("/error-details")
    def error_details():
        return {"error": f"Unexpected error: {str(e)}", "traceback": traceback.format_exc()}

# This ensures that Vercel can find the FastAPI application
# Vercel looks for a variable called 'app' in the module