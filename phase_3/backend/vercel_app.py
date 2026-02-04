# Minimal serverless-ready FastAPI app for Vercel
import os
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import sys
from typing import AsyncIterator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set default environment variables for Vercel
os.environ.setdefault("SECRET_KEY", "fallback-secret-key-change-in-production")
os.environ.setdefault("DATABASE_URL", "sqlite:///./vercel_fallback.db")
os.environ.setdefault("BETTER_AUTH_SECRET", "fallback-auth-secret-change-in-production")

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Lifespan event for Vercel compatibility"""
    logger.info("Starting up FastAPI app for Vercel")
    yield
    logger.info("Shutting down FastAPI app")

# Create FastAPI app with lifespan
app = FastAPI(lifespan=lifespan)

# CORS middleware for Vercel deployment
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For Vercel deployments, adjust as needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {
        "message": "AI-Powered Todo Chatbot API - Serverless Ready",
        "status": "operational",
        "platform": "vercel"
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "platform": "vercel",
        "serverless": True
    }


@app.get("/debug/test")
def debug_test():
    """Simple test endpoint to confirm basic functionality"""
    return {"test": "success", "message": "Backend is receiving requests properly", "platform": "vercel"}


@app.get("/debug/routes")
def debug_routes():
    """Debug endpoint to list all registered routes"""
    routes_info = []
    for route in app.routes:
        if hasattr(route, 'methods') and hasattr(route, 'path'):
            routes_info.append({
                "path": route.path,
                "methods": list(route.methods) if hasattr(route, 'methods') else ["UNKNOWN"]
            })

    return {
        "total_routes": len(routes_info),
        "routes": routes_info,
        "platform": "vercel",
        "serverless": True
    }

# Import routes with error handling
try:
    from src.api.auth import router as auth_router
    app.include_router(auth_router, prefix="/auth")
except ImportError as e:
    logger.error(f"Could not import auth router: {e}")

    @app.get("/auth/health")
    def auth_health():
        return {"status": "auth_router_not_loaded"}

try:
    from src.api.tasks import router as tasks_router
    app.include_router(tasks_router, prefix="/tasks")
except ImportError as e:
    logger.error(f"Could not import tasks router: {e}")

try:
    from src.api.chat import router as chat_router
    app.include_router(chat_router)
except ImportError as e:
    logger.error(f"Could not import chat router: {e}")

try:
    from src.api.dashboard import router as dashboard_router
    app.include_router(dashboard_router, prefix="/dashboard")
except ImportError as e:
    logger.error(f"Could not import dashboard router: {e}")

try:
    from src.api.analysis import router as analysis_router
    app.include_router(analysis_router, prefix="/analysis")
except ImportError as e:
    logger.error(f"Could not import analysis router: {e}")

# Error handler for Vercel
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Global exception: {exc}")
    return {"error": "Internal server error", "status": "crashed"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))