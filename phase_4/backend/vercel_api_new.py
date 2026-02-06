import sys
import os
import logging
import traceback

# Set up basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Log basic debugging information
logger.info(f"Current working directory: {os.getcwd()}")
logger.info(f"Python executable: {sys.executable}")
logger.info(f"Python version: {sys.version}")
logger.info(f"Working dir contents: {os.listdir('.')}")

try:
    # Import FastAPI first (most essential dependency)
    from fastapi import FastAPI
    logger.info("FastAPI imported successfully")
except ImportError as e:
    logger.error(f"Failed to import FastAPI: {e}")
    # If FastAPI isn't available, there's a bigger issue
    raise

# Create the app with minimal dependencies
app = FastAPI(
    title="AI-Powered Todo Chatbot API - Vercel Safe Mode",
    description="Safe mode API that prioritizes stability over features",
    version="1.0.0-safe"
)

logger.info("Basic FastAPI app created successfully")

# Basic CORS setup without complex logic
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173", "http://localhost:3000", "http://localhost:8000",
        "http://127.0.0.1:5173", "http://127.0.0.1:3000", "http://127.0.0.1:8000",
        "https://hackathon-2-p-3-frontend.vercel.app",
        "https://hackathon-2-p-3-backend.vercel.app",
        os.getenv("FRONTEND_URL", "https://hackathon-2-p-3-frontend.vercel.app")
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple routes that will always work
@app.get("/")
def read_root():
    return {
        "message": "API is running in safe mode",
        "status": "operational",
        "vercel_compatible": True
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "vercel-api", "timestamp": "now"}

@app.get("/status")
def status_check():
    return {
        "status": "operational",
        "vercel_compatible": True,
        "routes_count": len(app.routes),
        "working": True
    }

# Try to add more functionality from vercel_main if possible
try:
    # Import components individually from vercel_main
    from vercel_main import (
        api_health,
        catch_all_handler
    )

    # Register the routes
    app.add_api_route("/api/health", api_health, methods=["GET"])
    app.add_api_route("/{path_name:path}", catch_all_handler, methods=["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD"])

    logger.info("Additional routes from vercel_main loaded successfully")

except ImportError as e:
    logger.warning(f"Could not load additional routes from vercel_main: {e}")
    logger.info("Continuing with basic safe mode app")
except Exception as e:
    logger.warning(f"Error loading additional routes: {e}")
    logger.info("Continuing with basic safe mode app")

logger.info("Vercel API setup completed successfully")

# Export the app for Vercel
# This variable is what Vercel looks for