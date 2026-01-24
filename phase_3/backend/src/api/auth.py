from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
import logging
import uuid

logger = logging.getLogger(__name__)

router = APIRouter(tags=["authentication"])

# Define request models
class LoginRequestModel(BaseModel):
    email: str
    password: str

class RegisterRequestModel(BaseModel):
    email: str
    password: str
    name: str = None

# Simple in-memory user store for testing (will be replaced with DB later)
test_users = {}

@router.get("/test")
async def test_auth_endpoint():
    """Test endpoint to verify auth router is working"""
    return {
        "status": "✓ Auth endpoints are working",
        "message": "Bypass mode - no database required",
        "endpoints": [
            "POST /auth/login - Login with email/password",
            "POST /auth/register - Register new user",
            "GET /auth/test - This endpoint"
        ],
        "test_credentials": {
            "email": "test@example.com",
            "password": "password123"
        }
    }


@router.post("/login")
async def login(credentials: LoginRequestModel):
    """Login endpoint - BYPASS MODE"""
    try:
        logger.info(f"Login attempt for: {credentials.email}")
        
        # For testing: accept any login
        if not credentials.email or not credentials.password:
            raise HTTPException(status_code=400, detail="Email and password required")
        
        # Generate a fake token
        fake_token = f"token_{uuid.uuid4().hex[:20]}"
        
        return {
            "access_token": fake_token,
            "token_type": "bearer",
            "user": {
                "id": f"user_{uuid.uuid4().hex[:12]}",
                "email": credentials.email,
                "name": credentials.email.split("@")[0]
            }
        }
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Login failed: {str(e)}")


@router.post("/register")
async def register(credentials: RegisterRequestModel):
    """Register endpoint - BYPASS MODE"""
    try:
        logger.info(f"Register attempt for: {credentials.email}")
        
        if not credentials.email or not credentials.password:
            raise HTTPException(status_code=400, detail="Email and password required")
        
        # Generate fake data
        user_id = f"user_{uuid.uuid4().hex[:12]}"
        fake_token = f"token_{uuid.uuid4().hex[:20]}"
        
        return {
            "access_token": fake_token,
            "token_type": "bearer",
            "user": {
                "id": user_id,
                "email": credentials.email,
                "name": credentials.name or credentials.email.split("@")[0]
            }
        }
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Register error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")


@router.get("/me")
async def get_current_user_endpoint():
    """Get current user endpoint - BYPASS MODE"""
    try:
        # In bypass mode, return a dummy user
        return {
            "id": "user_bypass_mode",
            "email": "bypass@example.com",
            "name": "Bypass User"
        }
    except Exception as e:
        logger.error(f"Get user error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get user: {str(e)}")