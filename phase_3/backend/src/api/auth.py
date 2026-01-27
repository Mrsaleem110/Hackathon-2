from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
import logging
import uuid
from ..auth import require_auth, User as UserClass

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
    """Login endpoint - creates proper JWT token"""
    try:
        logger.info(f"Login attempt for: {credentials.email}")

        if not credentials.email or not credentials.password:
            raise HTTPException(status_code=400, detail="Email and password required")

        # In bypass mode, create a proper user session with JWT token
        from ..auth import create_user_session

        user_id = f"user_{uuid.uuid4().hex[:12]}"
        token = create_user_session(user_id, credentials.email, credentials.email.split("@")[0])

        return {
            "access_token": token,
            "token_type": "bearer",
            "user": {
                "id": user_id,
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
    """Register endpoint - creates proper JWT token"""
    try:
        logger.info(f"Register attempt for: {credentials.email}")

        if not credentials.email or not credentials.password:
            raise HTTPException(status_code=400, detail="Email and password required")

        # In bypass mode, create a proper user session with JWT token
        from ..auth import create_user_session

        user_id = f"user_{uuid.uuid4().hex[:12]}"
        token = create_user_session(user_id, credentials.email, credentials.name or credentials.email.split("@")[0])

        return {
            "access_token": token,
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
async def get_current_user_endpoint(current_user: UserClass = Depends(require_auth())):
    """Get current user endpoint - validates token and returns user info"""
    try:
        # Return the authenticated user's information
        return {
            "id": current_user.id,
            "email": current_user.email,
            "name": current_user.name
        }
    except Exception as e:
        logger.error(f"Get user error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get user: {str(e)}")