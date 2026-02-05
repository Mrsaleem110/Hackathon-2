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

# Enhanced CORS middleware for Vercel deployment with specific domains
frontend_url = os.getenv("FRONTEND_URL", "https://hackathon-2-p-3-frontend.vercel.app")
cors_origins_env = os.getenv("CORS_ORIGINS", "")

# Build the list of allowed origins
cors_origins = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:3000",
    "http://localhost:8000",
    "http://localhost:8080",
    "https://hackathon-2-p-3-frontend.vercel.app",  # Your specific frontend
    "https://hackathon-2-p-3-backend.vercel.app",   # Your backend domain
    "https://*.vercel.app",  # Wildcard for Vercel preview deployments
]

# Add frontend URL from environment
if frontend_url and frontend_url not in cors_origins:
    cors_origins.append(frontend_url)

# Add any additional origins from environment variable
if cors_origins_env:
    additional_origins = [origin.strip() for origin in cors_origins_env.split(",") if origin.strip()]
    for origin in additional_origins:
        if origin not in cors_origins:
            cors_origins.append(origin)

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
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

# Import routes with better error handling
# Import routes with better error handling
try:
    # Add the src directory to the path for proper imports
    import sys
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

    from src.api.auth import router as auth_router
    app.include_router(auth_router, prefix="/auth")
    logger.info("Auth router loaded successfully")
except ImportError as e:
    logger.error(f"Could not import auth router: {e}")
    logger.error(f"Available files in src/api/: {os.listdir('src/api/') if os.path.exists('src/api/') else 'Directory does not exist'}")

    @app.get("/auth/health")
    def auth_health():
        return {"status": "auth_router_not_loaded", "error": str(e)}

    @app.post("/auth/login")
    async def login_stub():
        return {"error": "Auth router not loaded", "message": str(e)}

    @app.post("/auth/register")
    async def register_stub():
        return {"error": "Auth router not loaded", "message": str(e)}

    @app.get("/auth/me")
    async def me_stub():
        return {"error": "Auth router not loaded", "message": str(e)}

try:
    from src.api.tasks import router as tasks_router
    app.include_router(tasks_router, prefix="/tasks")
    logger.info("Tasks router loaded successfully")
except ImportError as e:
    logger.error(f"Could not import tasks router: {e}")

    @app.get("/tasks")
    async def tasks_stub():
        return {"error": "Tasks router not loaded", "message": str(e)}

try:
    from src.api.chat import router as chat_router
    app.include_router(chat_router)
    logger.info("Chat router loaded successfully")
except ImportError as e:
    logger.error(f"Could not import chat router: {e}")

    @app.get("/")
    async def chat_stub():
        return {"error": "Chat router not loaded", "message": str(e)}

try:
    from src.api.dashboard import router as dashboard_router
    app.include_router(dashboard_router, prefix="/dashboard")
    logger.info("Dashboard router loaded successfully")
except ImportError as e:
    logger.error(f"Could not import dashboard router: {e}")

    @app.get("/dashboard")
    async def dashboard_stub():
        return {"error": "Dashboard router not loaded", "message": str(e)}

try:
    from src.api.analysis import router as analysis_router
    app.include_router(analysis_router, prefix="/analysis")
    logger.info("Analysis router loaded successfully")
except ImportError as e:
    logger.error(f"Could not import analysis router: {e}")

    @app.get("/analysis")
    async def analysis_stub():
        return {"error": "Analysis router not loaded", "message": str(e)}

# Error handler for Vercel
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Global exception: {exc}")
    return {"error": "Internal server error", "status": "crashed"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))