from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session
from typing import Optional
import uuid
from datetime import datetime
import logging
import os

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app early to prevent startup failures
app = FastAPI(
    title="AI-Powered Todo Chatbot API",
    description="API for the AI-Powered Todo Chatbot that enables users to manage tasks using natural language",
    version="1.0.0"
)

# Add CORS middleware
allowed_origins = ["http://localhost:5173", "http://localhost:5174", "http://localhost:3000", "http://127.0.0.1:5173", "http://127.0.0.1:5174", "http://127.0.0.1:3000"]

# In production, add the deployed frontend URL from environment variables
if os.getenv("VERCEL_ENV"):
    # When deployed to Vercel, allow the frontend URL if provided
    frontend_url = os.getenv("FRONTEND_URL")
    if frontend_url:
        allowed_origins.append(frontend_url)
    else:
        # Allow any vercel.app domain when deployed to Vercel
        allowed_origins.append("https://*.vercel.app")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,  # Allow frontend origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    # Expose authorization header for auth token
    expose_headers=["Access-Control-Allow-Origin", "Authorization"]
)

# Move imports inside try-catch to catch import errors during initialization
try:
    # Import models (removing duplicates)
    from ..models.task import Task, TaskCreate, TaskUpdate, TaskCreateRequest
    from ..models.conversation import Conversation, ConversationCreate
    from ..models.message import Message, MessageCreate, MessageRole
    from ..models.user import User, UserCreate, UserUpdate, UserPublic
    from ..database.connection import get_session, get_engine
    from ..services.task_service import TaskService
    from ..services.conversation_service import ConversationService
    from ..services.message_service import MessageService

    logger.info("All modules imported successfully")

except ImportError as e:
    logger.error(f"Import error during app initialization: {e}")
    # Add a basic error endpoint
    @app.get("/")
    def read_root():
        return {"error": f"App failed to initialize: {str(e)}"}

# Only include the startup event if not in serverless environment
if os.getenv("VERCEL_ENV") is None:
    @app.on_event("startup")
    async def startup_event():
        """Create database tables on startup"""
        try:
            logger.info("Initializing database tables...")
            from sqlmodel import SQLModel
            engine = get_engine()
            SQLModel.metadata.create_all(bind=engine)
            logger.info("Database tables initialized successfully!")
        except Exception as e:
            logger.error(f"Error initializing database tables: {e}")
            # Continue without raising the exception to allow the app to start
            # The database might be connected later when the first request comes

@app.get("/")
def read_root():
    return {"message": "AI-Powered Todo Chatbot API"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow()}

# Include the auth, tasks, chat, chatkit, and chatkit_agent routers
# Only include if imports were successful
try:
    from .auth import router as auth_router
    from .tasks import router as tasks_router
    from .chat import router as chat_router
    from .chatkit import router as chatkit_router
    from .chatkit_agent import router as chatkit_agent_router

    app.include_router(auth_router)
    app.include_router(tasks_router, prefix="/tasks")
    app.include_router(chat_router)
    app.include_router(chatkit_router)
    app.include_router(chatkit_agent_router)
except ImportError as e:
    logger.error(f"Router import error: {e}")

# This ensures the app is available when Vercel imports it
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)