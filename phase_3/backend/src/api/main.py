from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session
from typing import Optional
import uuid
from datetime import datetime

# Import models
from ..models.task import Task, TaskCreate, TaskUpdate
from ..models.conversation import Conversation, ConversationCreate
from ..models.message import Message, MessageCreate, MessageRole
from ..database.connection import get_session
from ..services.task_service import TaskService
from ..services.conversation_service import ConversationService
from ..services.message_service import MessageService

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