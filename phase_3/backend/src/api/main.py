from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response, JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
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

# BULLETPROOF CORS - Middleware approach
# Get frontend URL from environment variable for Vercel deployments
frontend_url = os.getenv("FRONTEND_URL", "https://hackathon-2-p-3.vercel.app")

cors_origins = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:5183",  # Added the port from the error message
    "http://localhost:3000",
    "http://localhost:8000",
    "http://localhost:8001",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:5174",
    "http://127.0.0.1:5183",  # Added the IPv4 equivalent
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8000",
    "http://127.0.0.1:8001",
    "https://hackathon-2-sooty.vercel.app",
    "https://hackathon-2-p-3.vercel.app",
    "https://hackathon-2-phase-3-backend.vercel.app",
    "https://hackathon-2-phase-3.vercel.app",
    frontend_url,
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ADDITIONAL: Override exception handler to ensure CORS headers on errors
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Add CORS headers to HTTP exceptions"""
    response = JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )
    origin = request.headers.get("origin", "*")
    response.headers["Access-Control-Allow-Origin"] = origin
    response.headers["Access-Control-Allow-Credentials"] = "true"
    return response

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle all other exceptions and return JSON"""
    import traceback
    response = JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "message": str(exc) if os.getenv("DEBUG", "").lower() == "true" else "An unexpected error occurred"
        },
    )
    origin = request.headers.get("origin", "*")
    response.headers["Access-Control-Allow-Origin"] = origin
    response.headers["Access-Control-Allow-Credentials"] = "true"
    return response

@app.exception_handler(StarletteHTTPException)
async def starlette_http_exception_handler(request, exc):
    """Handle Starlette HTTP exceptions and return JSON"""
    response = JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )
    origin = request.headers.get("origin", "*")
    response.headers["Access-Control-Allow-Origin"] = origin
    response.headers["Access-Control-Allow-Credentials"] = "true"
    return response

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    """Handle validation errors and return JSON"""
    response = JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": "Validation error",
            "errors": exc.errors()
        },
    )
    origin = request.headers.get("origin", "*")
    response.headers["Access-Control-Allow-Origin"] = origin
    response.headers["Access-Control-Allow-Credentials"] = "true"
    return response

# Handle OPTIONS preflight explicitly - match the origin from request
@app.options("/{full_path:path}")
async def preflight_handler(request, full_path: str):
    """Handle CORS preflight requests"""
    response = Response()
    origin = request.headers.get("origin", "")

    # For development, allow localhost origins dynamically
    if origin and (origin.startswith("http://localhost:") or origin.startswith("http://127.0.0.1:")):
        response.headers["Access-Control-Allow-Origin"] = origin
    # Otherwise, check if the origin is in our allowed list
    elif origin in cors_origins:
        response.headers["Access-Control-Allow-Origin"] = origin
    # If origin is not allowed, we don't set the header, letting the default CORS middleware handle it

    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS, PATCH, HEAD"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization, X-Requested-With, Accept, Origin"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Max-Age"] = "3600"
    return response

# Add middleware to ensure all responses have proper Content-Type header
@app.middleware("http")
async def ensure_json_response_middleware(request: Request, call_next):
    """Middleware to ensure responses are JSON when appropriate"""
    try:
        response = await call_next(request)
        
        # If response doesn't have a content-type or it's not JSON, and it's an API endpoint, set it to JSON
        content_type = response.headers.get('content-type', '')
        path = request.url.path
        
        # For API endpoints that don't have content-type set, ensure it's JSON
        if path.startswith('/api') or path.startswith('/auth') or path.startswith('/tasks') or path.startswith('/chat') or path.startswith('/dashboard') or path.startswith('/analysis'):
            if not content_type or 'text/html' in content_type:
                response.headers['content-type'] = 'application/json'
        
        return response
    except Exception as e:
        # If there's an error in middleware, return JSON error response
        logger.error(f"Middleware error: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error", "error": str(e) if os.getenv("DEBUG", "").lower() == "true" else "An unexpected error occurred"}
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
        "allowed_origins_list": [
            "http://localhost:5173", "http://localhost:5174", "http://localhost:3000",
            "http://localhost:8000", "http://localhost:8001", "http://127.0.0.1:5173",
            "http://127.0.0.1:5174", "http://127.0.0.1:3000", "http://127.0.0.1:8000",
            "http://127.0.0.1:8001", "https://hackathon-2-sooty.vercel.app",
            "https://hackathon-2-p-3.vercel.app", "https://hackathon-2-phase-3-backend.vercel.app",
            "https://hackathon-2-phase-3.vercel.app"
        ]
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
except Exception as e:
    logger.error(f"Failed to import/include tasks router: {e}")
    logger.error(f"Error type: {type(e).__name__}")
    import traceback
    logger.error(f"Traceback: {traceback.format_exc()}")

try:
    from .dashboard import router as dashboard_router
    logger.info("Successfully imported dashboard router")
    app.include_router(dashboard_router, prefix="/dashboard")
    logger.info("Successfully included dashboard router")
except Exception as e:
    logger.error(f"Failed to import/include dashboard router: {e}")
    logger.error(f"Error type: {type(e).__name__}")
    import traceback
    logger.error(f"Traceback: {traceback.format_exc()}")

try:
    from .analysis import router as analysis_router
    logger.info("Successfully imported analysis router")
    app.include_router(analysis_router, prefix="/analysis")
    logger.info("Successfully included analysis router")
except Exception as e:
    logger.error(f"Failed to import/include analysis router: {e}")
    logger.error(f"Error type: {type(e).__name__}")
    import traceback
    logger.error(f"Traceback: {traceback.format_exc()}")

try:
    from .chat import router as chat_router
    logger.info("Successfully imported chat router")
    app.include_router(chat_router)
    logger.info("Successfully included chat router")
except Exception as e:
    logger.error(f"Failed to import/include chat router: {e}")
    logger.error(f"Error type: {type(e).__name__}")
    import traceback
    logger.error(f"Traceback: {traceback.format_exc()}")

try:
    from .chatkit import router as chatkit_router
    logger.info("Successfully imported chatkit router")
    app.include_router(chatkit_router)
    logger.info("Successfully included chatkit router")
except Exception as e:
    logger.error(f"Failed to import/include chatkit router: {e}")
    logger.error(f"Error type: {type(e).__name__}")
    import traceback
    logger.error(f"Traceback: {traceback.format_exc()}")

try:
    from .chatkit_agent import router as chatkit_agent_router
    logger.info("Successfully imported chatkit_agent router")
    app.include_router(chatkit_agent_router)
    logger.info("Successfully included chatkit_agent router")
except Exception as e:
    logger.error(f"Failed to import/include chatkit_agent router: {e}")
    logger.error(f"Error type: {type(e).__name__}")
    import traceback
    logger.error(f"Traceback: {traceback.format_exc()}")


# Add a catch-all 404 handler to return JSON instead of HTML
@app.api_route("/{path_name:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD"])
async def catch_all_handler(path_name: str):
    """Catch-all handler for undefined routes - returns JSON 404 instead of HTML"""
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Route '/{path_name}' not found"
    )


# This ensures the app is available when Vercel imports it
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)