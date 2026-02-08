import sys
import os
import logging
from fastapi import FastAPI
from fastapi.responses import JSONResponse

# Set up basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Log basic information
logger.info("Minimal Vercel API starting...")
logger.info(f"Current working directory: {os.getcwd()}")
logger.info(f"Python executable: {sys.executable}")
logger.info(f"Python version: {sys.version}")

# Create a minimal FastAPI app that will definitely work
app = FastAPI(title="Minimal API", description="Minimal working API for Vercel", version="1.0.0")

@app.get("/")
def read_root():
    return {"message": "Minimal API is working", "status": "operational"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "minimal-api"}

@app.get("/status")
def status_check():
    return {
        "status": "success",
        "service": "minimal-api",
        "working": True
    }

# Export the app for Vercel
logger.info("Minimal Vercel API initialized successfully")