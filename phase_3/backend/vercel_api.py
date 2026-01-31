import sys
import os
import logging
from typing import Optional

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
    from fastapi import FastAPI, HTTPException, Depends
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import JSONResponse
    from pydantic import BaseModel

    # Create app with minimal setup
    app = FastAPI(
        title="AI-Powered Todo Chatbot API - Auth Compatible",
        description="API with essential auth routes for frontend compatibility",
        version="1.0.0-auth-compatible"
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

    # Pydantic models for auth
    class UserLogin(BaseModel):
        email: str
        password: str

    class UserRegister(BaseModel):
        email: str
        password: str
        name: str

    # Basic routes that will always work
    @app.get("/")
    def read_root():
        return {
            "message": "Auth-compatible API is running",
            "status": "operational",
            "vercel_compatible": True,
            "notes": "This version includes essential auth routes for frontend compatibility."
        }

    @app.get("/health")
    def health_check():
        return {"status": "healthy", "service": "auth-compatible-api", "timestamp": "now"}

    @app.get("/status")
    def status_check():
        return {
            "status": "operational",
            "mode": "auth-compatible",
            "working": True,
            "routes_count": len(app.routes)
        }

    # Essential authentication routes for frontend compatibility
    @app.post("/auth/login")
    def login(user_login: UserLogin):
        return {
            "status": "error",
            "message": "Auth service temporarily unavailable. Please configure environment variables in Vercel dashboard.",
            "needs_configuration": True,
            "hint": "Set DATABASE_URL and SECRET_KEY in Vercel environment variables"
        }

    @app.post("/auth/register")
    def register(user_register: UserRegister):
        return {
            "status": "error",
            "message": "Auth service temporarily unavailable. Please configure environment variables in Vercel dashboard.",
            "needs_configuration": True,
            "hint": "Set DATABASE_URL and SECRET_KEY in Vercel environment variables"
        }

    @app.get("/auth/me")
    def get_current_user():
        return {
            "status": "error",
            "message": "Auth service temporarily unavailable. Please configure environment variables in Vercel dashboard.",
            "needs_configuration": True,
            "hint": "Set DATABASE_URL and SECRET_KEY in Vercel environment variables"
        }

    @app.post("/auth/logout")
    def logout():
        return {
            "status": "success",
            "message": "Logged out successfully"
        }

    # Task-related routes for frontend compatibility
    @app.get("/tasks")
    def get_tasks():
        # Return an empty array to prevent "filter is not a function" error in frontend
        return []

    @app.post("/tasks")
    def create_task():
        return {
            "id": None,
            "title": "Configuration Required",
            "description": "Task service temporarily unavailable. Please configure environment variables in Vercel dashboard.",
            "status": "error",
            "needs_configuration": True,
            "message": "Task service temporarily unavailable. Please configure environment variables in Vercel dashboard."
        }

    # Chat-related routes for frontend compatibility
    @app.post("/chat")
    def chat():
        # Return a structure that matches what frontend expects
        return {
            "response": "Chat service temporarily unavailable. Please configure environment variables in Vercel dashboard.",
            "conversationId": None,
            "timestamp": "now",
            "needs_configuration": True,
            "message": "Chat service temporarily unavailable. Please configure environment variables in Vercel dashboard."
        }

    # Dashboard and analysis routes - return data structures that match frontend expectations
    @app.get("/dashboard/stats")
    def dashboard_stats():
        # Return the data structure that frontend expects to avoid "filter is not a function" error
        return {
            "totalTasks": 0,
            "completedTasks": 0,
            "pendingTasks": 0,
            "overdueTasks": 0,
            "tasksByPriority": [],
            "tasksByCategory": [],
            "weeklyProgress": [],
            "monthlyStats": {},
            "needsConfiguration": True,
            "message": "Dashboard service temporarily unavailable. Please configure environment variables in Vercel dashboard."
        }

    @app.get("/analysis/user-insights")
    def user_insights():
        # Return the data structure that frontend expects
        return {
            "productivityInsights": [],
            "usagePatterns": {},
            "recommendations": [],
            "trends": {},
            "needsConfiguration": True,
            "message": "Analysis service temporarily unavailable. Please configure environment variables in Vercel dashboard."
        }

    logger.info("Auth-compatible API created successfully")

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