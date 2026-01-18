from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session
from typing import Optional
import uuid
from datetime import datetime
import logging

# Import models
from ..models.task import Task, TaskCreate, TaskUpdate
from ..models.conversation import Conversation, ConversationCreate
from ..models.message import Message, MessageCreate, MessageRole
from ..database.connection import get_session, get_engine
from ..services.task_service import TaskService
from ..services.conversation_service import ConversationService
from ..services.message_service import MessageService

# Import SQLModel table classes to register them with the metadata
from ..models.user import User, UserCreate, UserUpdate, UserPublic
from ..models.task import Task, TaskCreate, TaskUpdate, TaskCreateRequest
from ..models.conversation import Conversation, ConversationCreate
from ..models.message import Message, MessageCreate, MessageRole

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="AI-Powered Todo Chatbot API",
    description="API for the AI-Powered Todo Chatbot that enables users to manage tasks using natural language",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174", "http://localhost:3000", "http://127.0.0.1:5173", "http://127.0.0.1:5174", "http://127.0.0.1:3000", "*"],  # Allow frontend origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    # Expose authorization header for auth token
    expose_headers=["Access-Control-Allow-Origin", "Authorization"]
)

@app.on_event("startup")
async def startup_event():
    """Create database tables on startup"""
    try:
        logger.info("Initializing database tables...")
        from sqlmodel import SQLModel
        # Create engine and initialize tables
        engine = get_engine()
        # Create all tables defined in the models
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

# This ensures the app is available when Vercel imports it
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)