# Minimal FastAPI app for Vercel deployment - No external dependencies
import os
import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime, timedelta
from contextlib import asynccontextmanager
from typing import AsyncIterator
import hashlib
import secrets

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set environment variables defaults
os.environ.setdefault("SECRET_KEY", "fallback-secret-key-change-in-production")

# Simple in-memory user store for serverless demo (replace with proper DB in production)
users_db = {}

def simple_hash(password: str) -> str:
    """Simple hash function without external dependencies"""
    return hashlib.sha256(password.encode()).hexdigest()

def simple_verify_password(plain_password: str, hashed_password: str) -> bool:
    """Simple password verification without external dependencies"""
    return simple_hash(plain_password) == hashed_password

def simple_create_token(username: str) -> str:
    """Simple token creation without external dependencies"""
    # Create a simple token (in production, use proper JWT)
    token_data = f"{username}:{datetime.utcnow().isoformat()}:{secrets.token_hex(16)}"
    return hashlib.sha256(token_data.encode()).hexdigest()

def authenticate_user(username: str, password: str):
    """Authenticate user without external dependencies"""
    if username in users_db:
        user = users_db[username]
        if simple_verify_password(password, user["hashed_password"]):
            return user
    return None

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Lifespan event for Vercel compatibility"""
    logger.info("Starting up minimal FastAPI app for Vercel")
    yield
    logger.info("Shutting down minimal FastAPI app")

# Create FastAPI app with lifespan
app = FastAPI(lifespan=lifespan, title="Minimal API for Vercel")

# CORS middleware for Vercel deployment
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://hackathon-2-p-3-frontend.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str

@app.get("/")
def read_root():
    return {
        "message": "Minimal AI-Powered Todo Chatbot API - Serverless Ready",
        "status": "operational",
        "platform": "vercel",
        "features": ["auth", "health", "debug"]
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "platform": "vercel",
        "serverless": True,
        "timestamp": datetime.utcnow().isoformat()
    }

@app.post("/auth/login", response_model=LoginResponse)
async def login(login_request: LoginRequest):
    """Simple login endpoint for testing"""
    logger.info(f"Login attempt for user: {login_request.username}")

    # For testing purposes, create a default user if none exists
    if not users_db:
        users_db["admin"] = {
            "username": "admin",
            "hashed_password": simple_hash("admin123"),  # Default password
            "email": "admin@example.com"
        }
        logger.info("Created default admin user for testing")

    user = authenticate_user(login_request.username, login_request.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = simple_create_token(user["username"])

    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/auth/register")
async def register(login_request: LoginRequest):
    """Simple registration endpoint for testing"""
    if login_request.username in users_db:
        raise HTTPException(status_code=400, detail="Username already registered")

    hashed_password = simple_hash(login_request.password)
    users_db[login_request.username] = {
        "username": login_request.username,
        "hashed_password": hashed_password,
        "email": f"{login_request.username}@example.com"
    }

    # Return login response after registration
    access_token = simple_create_token(login_request.username)

    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/auth/me")
async def read_users_me():
    """Simple endpoint to test authentication"""
    return {"username": "test_user", "authenticated": True}

@app.get("/debug/test")
def debug_test():
    """Simple test endpoint to confirm basic functionality"""
    return {
        "test": "success",
        "message": "Backend is receiving requests properly",
        "platform": "vercel",
        "endpoints": ["/", "/health", "/auth/login", "/auth/register", "/auth/me", "/debug/test"]
    }

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

# Error handlers
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Global exception: {exc}")
    return {"error": "Internal server error", "status": "crashed", "message": str(exc)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))