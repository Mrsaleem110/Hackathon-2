import sys
import os
import logging

# Set up basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Log basic debugging information
logger.info(f"Current working directory: {os.getcwd()}")
logger.info(f"Python executable: {sys.executable}")
logger.info(f"Python version: {sys.version}")
logger.info(f"Working dir contents: {os.listdir('.')}")

# Create the simplest possible FastAPI app that will definitely work
try:
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import JSONResponse

    # Create app with minimal setup
    app = FastAPI(
        title="AI-Powered Todo Chatbot API - Emergency Fallback",
        description="Minimal API that always works on Vercel",
        version="1.0.0-emergency"
    )

    # Simple CORS middleware
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

    # Basic routes that will always work
    @app.get("/")
    def read_root():
        return {
            "message": "Emergency fallback API is running",
            "status": "operational",
            "vercel_compatible": True,
            "notes": "This is a minimal version to prevent crashes. Please configure proper environment variables."
        }

    @app.get("/health")
    def health_check():
        return {"status": "healthy", "service": "fallback-api", "timestamp": "now"}

    @app.get("/status")
    def status_check():
        return {
            "status": "operational",
            "mode": "emergency-fallback",
            "working": True,
            "routes_count": 3  # /, /health, /status
        }

    @app.get("/api/health")
    def api_health():
        return {"status": "operational", "service": "api", "fallback": True}

    logger.info("Emergency fallback API created successfully")

except Exception as e:
    # If even this minimal setup fails, we have a serious problem
    # But we still need to export an app object for Vercel
    logger.error(f"Even minimal setup failed: {e}")

    # Create the most basic possible app using a different approach
    import fastapi
    app = fastapi.FastAPI()

    @app.get("/")
    def emergency_root():
        return {
            "status": "critical-error",
            "message": "Critical initialization error",
            "error": str(e) if str(e) else "Unknown error occurred"
        }

logger.info("Vercel API initialization completed")

# This ensures that Vercel can find the FastAPI application
# Vercel looks for a variable called 'app' in the module