# Minimal FastAPI app for Vercel deployment
import os
import logging
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from sqlmodel import Field, SQLModel, create_engine, Session, select
from contextlib import asynccontextmanager
from typing import AsyncIterator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set environment variables defaults
os.environ.setdefault("SECRET_KEY", "fallback-secret-key-change-in-production")
os.environ.setdefault("DATABASE_URL", "sqlite:///./minimal_fallback.db")
os.environ.setdefault("BETTER_AUTH_SECRET", "fallback-auth-secret-change-in-production")

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT settings
SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Simple in-memory user store for serverless demo (replace with proper DB in production)
users_db = {}

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def authenticate_user(username: str, password: str):
    # In a real app, this would query the database
    if username in users_db:
        user = users_db[username]
        if verify_password(password, user["hashed_password"]):
            return user
    return None

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

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
            "hashed_password": get_password_hash("admin123"),  # Default password
            "email": "admin@example.com"
        }
        logger.info("Created default admin user for testing")

    user = authenticate_user(login_request.username, login_request.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/auth/register")
async def register(login_request: LoginRequest):
    """Simple registration endpoint for testing"""
    if login_request.username in users_db:
        raise HTTPException(status_code=400, detail="Username already registered")

    hashed_password = get_password_hash(login_request.password)
    users_db[login_request.username] = {
        "username": login_request.username,
        "hashed_password": hashed_password,
        "email": f"{login_request.username}@example.com"
    }

    # Return login response after registration
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": login_request.username}, expires_delta=access_token_expires
    )

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