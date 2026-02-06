# Minimal Vercel-compatible API
import os
from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response, JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from typing import Optional
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app early to prevent startup failures
app = FastAPI(
    title="AI-Powered Todo Chatbot API - Vercel Optimized",
    description="Lightweight version optimized for Vercel serverless functions",
    version="1.0.0"
)

# CORS setup - simplified for Vercel
frontend_url = os.getenv("FRONTEND_URL", "https://hackathon-2-p-3-frontend.vercel.app")
cors_origins = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:5173",
    "http://localhost:3000",
    "http://localhost:8000",
    "http://localhost:8001",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:5174",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8000",
    "http://127.0.0.1:8001",
    "https://hackathon-2-sooty.vercel.app",
    "https://hackathon-2-p-3.vercel.app",
    "https://hackathon-2-p-3-frontend.vercel.app",
    "https://hackathon-2-p-3-frontend-k57stbf9j.vercel.app",
    "https://hackathon-2-p-3-backend.vercel.app",
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

# Error handlers
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

# Handle OPTIONS preflight
@app.options("/{full_path:path}")
async def preflight_handler(request, full_path: str):
    """Handle CORS preflight requests"""
    response = Response()
    origin = request.headers.get("origin", "")

    # Check if the request is from a Vercel preview deployment (dynamic subdomains)
    if origin and ".vercel.app" in origin:
        allowed_vercel_domains = [
            "hackathon-2-p-3-frontend.vercel.app",
            "hackathon-2-p-3-backend.vercel.app",
            "hackathon-2-phase-3-backend.vercel.app",
            "hackathon-2-phase-3.vercel.app",
            "hackathon-2-sooty.vercel.app",
            "hackathon-2-p-3.vercel.app"
        ]
        is_allowed_vercel = any(origin.endswith(domain) for domain in allowed_vercel_domains)

        if is_allowed_vercel:
            response.headers["Access-Control-Allow-Origin"] = origin
    elif origin and (origin.startswith("http://localhost:") or origin.startswith("http://127.0.0.1:")):
        response.headers["Access-Control-Allow-Origin"] = origin
    elif origin in cors_origins:
        response.headers["Access-Control-Allow-Origin"] = origin

    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS, PATCH, HEAD"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization, X-Requested-With, Accept, Origin"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Max-Age"] = "86400"
    return response

# Middleware for CORS
@app.middleware("http")
async def cors_and_content_type_middleware(request: Request, call_next):
    """Middleware to ensure all responses have proper CORS headers"""
    if request.method == "OPTIONS":
        response = Response()
        origin = request.headers.get("origin", "")

        if origin and ".vercel.app" in origin:
            allowed_vercel_domains = [
                "hackathon-2-p-3-frontend.vercel.app",
                "hackathon-2-p-3-backend.vercel.app",
                "hackathon-2-phase-3-backend.vercel.app",
                "hackathon-2-phase-3.vercel.app",
                "hackathon-2-sooty.vercel.app",
                "hackathon-2-p-3.vercel.app"
            ]
            is_allowed_vercel = any(origin.endswith(domain) for domain in allowed_vercel_domains)

            if is_allowed_vercel or origin in cors_origins:
                response.headers["Access-Control-Allow-Origin"] = origin
        elif origin and (origin.startswith("http://localhost:") or origin.startswith("http://127.0.0.1:")):
            response.headers["Access-Control-Allow-Origin"] = origin
        elif origin in cors_origins:
            response.headers["Access-Control-Allow-Origin"] = origin

        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS, PATCH, HEAD"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization, X-Requested-With, Accept, Origin"
        response.headers["Access-Control-Allow-Credentials"] = "true"
        response.headers["Access-Control-Max-Age"] = "86400"
        return response

    response = await call_next(request)

    # Add CORS headers to all responses
    origin = request.headers.get("origin", "")
    if origin and ".vercel.app" in origin:
        allowed_vercel_domains = [
            "hackathon-2-p-3-frontend.vercel.app",
            "hackathon-2-p-3-backend.vercel.app",
            "hackathon-2-phase-3-backend.vercel.app",
            "hackathon-2-phase-3.vercel.app",
            "hackathon-2-sooty.vercel.app",
            "hackathon-2-p-3.vercel.app"
        ]
        is_allowed_vercel = any(origin.endswith(domain) for domain in allowed_vercel_domains)

        if is_allowed_vercel or origin in cors_origins:
            response.headers["Access-Control-Allow-Origin"] = origin
    elif origin and (origin.startswith("http://localhost:") or origin.startswith("http://127.0.0.1:")):
        response.headers["Access-Control-Allow-Origin"] = origin
    elif origin in cors_origins:
        response.headers["Access-Control-Allow-Origin"] = origin

    response.headers["Access-Control-Allow-Credentials"] = "true"
    return response

# Basic routes
@app.get("/")
def read_root():
    return {"message": "Vercel-optimized API", "status": "operational", "version": "1.0.0"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": "now", "routes_count": len(app.routes)}

@app.get("/status")
def status_check():
    route_paths = [getattr(route, 'path', 'unknown') for route in app.routes]
    return {
        "status": "operational",
        "version": "1.0.0",
        "total_routes": len(app.routes),
        "all_routes": route_paths
    }

# Placeholder routes - will be implemented when the full app loads
@app.get("/api/health")
def api_health():
    return {"status": "operational", "service": "api", "vercel_optimized": True}

# Catch-all handler
@app.api_route("/{path_name:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD"])
async def catch_all_handler(path_name: str):
    """Catch-all handler for undefined routes"""
    return {
        "status": "info",
        "message": f"Route '/{path_name}' is not yet implemented in Vercel-optimized mode",
        "hint": "This is a lightweight version optimized for Vercel deployment"
    }