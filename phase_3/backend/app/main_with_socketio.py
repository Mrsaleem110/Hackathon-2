from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .chat.routes import router as chat_router
from .api.v1.auth import router as auth_router
from .db.database import engine
from .models.conversation import Conversation, Message  # Import models to register them
from sqlmodel import SQLModel
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Create FastAPI app
app = FastAPI(title="Todo AI Chat API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, configure this properly
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include auth and chat routes
app.include_router(auth_router)
app.include_router(chat_router)

# Create database tables
@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

@app.get("/")
def read_root():
    return {"message": "Todo AI Chat API is running!"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

# Import and integrate Socket.IO server
from fastapi_socketio import SocketManager
from .chat.socketio_server import sio

# Initialize Socket.IO manager
socket_manager = SocketManager(app=app, mount_location="/socket.io/")