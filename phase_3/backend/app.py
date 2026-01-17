# Vercel entry point for FastAPI application
import sys
import os

# Add the src directory to the path so imports work correctly
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import the FastAPI app from the main module
from src.api.main import app

# This ensures that Vercel can find the FastAPI application
# Vercel looks for a variable called 'app' in the module