from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
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

# Add CORS middleware - use built-in CORSMiddleware for better reliability
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174", 
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
        "http://127.0.0.1:3000",
        "https://hackathon-2-sooty.vercel.app",
        "https://hackathon-2-p-3.vercel.app",
        "https://hackathon-2-phase-3-backend.vercel.app",
        "https://hackathon-2-phase-3.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Get additional origins from environment
additional_origins = os.getenv("ADDITIONAL_ALLOWED_ORIGINS", "")
if additional_origins:
    for origin in additional_origins.split(","):
        origin = origin.strip()
        if origin and origin not in app.user_middleware[0].kwargs.get("allow_origins", []):
            app.user_middleware[0].kwargs["allow_origins"].append(origin)

# Custom CORS middleware as fallback - simplified version
allowed_origins = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:3000",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:5174",
    "http://127.0.0.1:3000",
    "https://hackathon-2-sooty.vercel.app",
    "https://hackathon-2-p-3.vercel.app",
    "https://hackathon-2-phase-3-backend.vercel.app",
    "https://hackathon-2-phase-3.vercel.app",
]

# Add simple HTTP middleware for additional header handling if needed
@app.middleware("http")
async def add_additional_headers(request, call_next):
    response = await call_next(request)
    # The CORSMiddleware above should handle CORS, this just adds any extra headers
    return response

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,  # Allow frontend origins
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],  # Explicitly include OPTIONS
    allow_headers=["*"],  # Allow all headers including Content-Type
    # Expose authorization and origin headers for auth token and CORS
    expose_headers=["Access-Control-Allow-Origin", "Authorization", "X-Total-Count", "Content-Type"]
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
    return {"message": "AI-Powered Todo Chatbot API", "status": "operational"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow(), "routes_count": len(app.routes)}

@app.get("/debug/routes")
def debug_routes():
    """Debug endpoint to list all registered routes"""
    routes_info = []
    for route in app.routes:
        if hasattr(route, 'methods') and hasattr(route, 'path'):
            routes_info.append({
                "path": route.path,
                "methods": list(route.methods) if route.methods else ["UNKNOWN"]
            })
    
    # Specifically show auth routes
    auth_routes = [r for r in routes_info if 'auth' in r['path'].lower()]
    
    return {
        "total_routes": len(routes_info), 
        "auth_routes": auth_routes,
        "all_routes": routes_info
    }

@app.get("/debug/test")
def debug_test():
    """Simple test endpoint to confirm basic functionality"""
    return {"test": "success", "message": "Backend is receiving requests properly"}

@app.get("/debug/cors")
def debug_cors():
    """Debug endpoint to test CORS configuration"""
    import os
    return {
        "cors_allowed_origins": os.getenv("ADDITIONAL_ALLOWED_ORIGINS", ""),
        "vercel_env": os.getenv("VERCEL_ENV"),
        "request_processing": "CORS middleware should be active",
        "allowed_origins_list": allowed_origins
    }

# Include the auth, tasks, chat, chatkit, and chatkit_agent routers
# Log each import for debugging
try:
    from .auth import router as auth_router
    logger.info("Successfully imported auth router")
    app.include_router(auth_router, prefix="/auth")
    logger.info("Successfully included auth router")
except Exception as e:
    logger.error(f"Failed to import/include auth router: {e}")
    logger.error(f"Error type: {type(e).__name__}")
    import traceback
    logger.error(f"Traceback: {traceback.format_exc()}")

try:
    from .tasks import router as tasks_router
    logger.info("Successfully imported tasks router")
    app.include_router(tasks_router, prefix="/tasks")
    logger.info("Successfully included tasks router")
except ImportError as e:
    logger.error(f"Failed to import tasks router: {e}")

try:
    from .chat import router as chat_router
    logger.info("Successfully imported chat router")
    app.include_router(chat_router)
    logger.info("Successfully included chat router")
except ImportError as e:
    logger.error(f"Failed to import chat router: {e}")

try:
    from .chatkit import router as chatkit_router
    logger.info("Successfully imported chatkit router")
    app.include_router(chatkit_router)
    logger.info("Successfully included chatkit router")
except ImportError as e:
    logger.error(f"Failed to import chatkit router: {e}")

try:
    from .chatkit_agent import router as chatkit_agent_router
    logger.info("Successfully imported chatkit_agent router")
    app.include_router(chatkit_agent_router)
    logger.info("Successfully included chatkit_agent router")
except ImportError as e:
    logger.error(f"Failed to import chatkit_agent router: {e}")

# This ensures the app is available when Vercel imports it
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)