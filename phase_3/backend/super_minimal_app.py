# Super minimal FastAPI app for Vercel - No external dependencies
import os
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import hashlib
import secrets

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(title="Super Minimal API for Vercel")

# CORS middleware for Vercel deployment - allow all for testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins temporarily for testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple in-memory storage
users_db = {}

class LoginRequest(BaseModel):
    username: str = None
    email: str = None  # Allow email as well
    password: str

    def get_username(self) -> str:
        # Use username if provided, otherwise use email
        return self.username if self.username else self.email

class LoginResponse(BaseModel):
    access_token: str
    token_type: str

@app.get("/")
def read_root():
    return {
        "message": "Super Minimal API - Serverless Ready",
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

@app.post("/auth/login")
async def login(request: LoginRequest):
    """Simple login endpoint - accepts both username and email"""
    # Create default user if none exists
    if not users_db:
        users_db["admin"] = {
            "username": "admin",
            "email": "admin@example.com",  # Add email for compatibility
            "password_hash": hashlib.sha256("admin123".encode()).hexdigest()
        }
        # Also create a user with email as key for email login
        users_db["admin@example.com"] = users_db["admin"]

    # Get the identifier (either username or email)
    identifier = request.get_username()

    # Check credentials
    password_hash = hashlib.sha256(request.password.encode()).hexdigest()
    if (identifier in users_db and
        users_db[identifier]["password_hash"] == password_hash):

        # Generate simple token
        token = hashlib.sha256(f"{identifier}_{secrets.token_hex(8)}".encode()).hexdigest()

        # Return in the expected format
        return {
            "access_token": token,
            "token_type": "bearer",
            "user": {
                "id": identifier,
                "username": identifier,
                "email": users_db[identifier].get("email", f"{identifier}@example.com")
            }
        }
    else:
        # Return proper error format
        from fastapi import status
        from fastapi.responses import JSONResponse
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "Invalid credentials"}
        )

class RegisterRequest(BaseModel):
    username: str = None
    email: str = None  # Allow email as well
    password: str

    def get_identifier(self) -> str:
        # Use username if provided, otherwise use email
        return self.username if self.username else self.email

@app.post("/auth/register")
async def register(request: RegisterRequest):
    """Simple registration endpoint - accepts both username and email"""
    identifier = request.get_identifier()

    if identifier in users_db:
        from fastapi import status
        from fastapi.responses import JSONResponse
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "User already exists"}
        )

    # Register new user
    users_db[identifier] = {
        "username": identifier,
        "email": request.email if request.email else identifier,
        "password_hash": hashlib.sha256(request.password.encode()).hexdigest()
    }

    # Generate token for new user
    token = hashlib.sha256(f"{identifier}_{secrets.token_hex(8)}".encode()).hexdigest()

    # Return in the expected format
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": identifier,
            "username": identifier,
            "email": request.email if request.email else f"{identifier}@example.com"
        }
    }

@app.get("/auth/me")
async def get_current_user():
    """Return current user info"""
    return {"username": "test_user", "authenticated": True}

@app.get("/debug/test")
def debug_test():
    """Test endpoint"""
    return {"test": "success", "message": "Backend working"}

# Global exception handler
@app.middleware("http")
async def error_handler(request, call_next):
    try:
        response = await call_next(request)
        return response
    except Exception as e:
        logger.error(f"Error in request: {e}")
        return {"error": "Internal server error", "message": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))