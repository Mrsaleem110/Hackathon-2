import sys
import os
import logging

# Add the src directory to the path so imports work correctly
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Set up basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    # Import the FastAPI app from the main module
    from src.api.main import app
    logger.info("FastAPI app imported successfully")
except ImportError as e:
    logger.error(f"Import error: {e}")
    # Create a simple fallback app for error reporting
    from fastapi import FastAPI
    app = FastAPI()

    @app.get("/")
    def read_root():
        return {"error": f"Failed to import app: {str(e)}"}

# This ensures that Vercel can find the FastAPI application
# Vercel looks for a variable called 'app' in the module