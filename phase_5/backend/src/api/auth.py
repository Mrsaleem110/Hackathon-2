from fastapi import APIRouter, HTTPException, status, Depends, Request
from pydantic import BaseModel
import logging
import uuid
from sqlmodel import Session
from ..auth import require_auth, User as AuthUser, authenticate_user, register_user as register_db_user
from ..database.connection import get_session
from ..models.user import UserCreate

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

@router.get("/test")
async def test_auth_endpoint():
    """Test endpoint to verify auth router is working"""
    return {
        "status": "✓ Auth endpoints are working",
        "message": "Authentication system is operational",
        "endpoints": [
            "POST /auth/login - Login with email/password",
            "POST /auth/register - Register new user",
            "GET /auth/me - Get current user info",
            "GET /auth/test - This endpoint"
        ]
    }


@router.post("/login")
async def login(credentials: LoginRequestModel, session: Session = Depends(get_session)):
    """Login endpoint - authenticates user and returns JWT token"""
    try:
        logger.info(f"Login attempt for: {credentials.email}")

        if not credentials.email or not credentials.password:
            raise HTTPException(status_code=400, detail="Email and password required")

        # Try to authenticate user against the database
        user = authenticate_user(credentials.email, credentials.password, session)

        if not user:
            raise HTTPException(status_code=401, detail="Incorrect email or password")

        # Create a proper user session with JWT token
        from ..auth import create_user_session
        token = create_user_session(user.id, user.email, user.name)

        return {
            "access_token": token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "email": user.email,
                "name": user.name
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Login failed: {str(e)}")


@router.post("/register")
async def register(credentials: RegisterRequestModel, session: Session = Depends(get_session)):
    """Register endpoint - registers new user and returns JWT token"""
    try:
        logger.info(f"Register attempt for: {credentials.email}")

        if not credentials.email or not credentials.password:
            raise HTTPException(status_code=400, detail="Email and password required")

        # Create user data object
        user_create_data = UserCreate(
            email=credentials.email,
            password=credentials.password,
            name=credentials.name or credentials.email.split("@")[0]
        )

        # Register user in the database
        user = register_db_user(user_create_data, session)

        # Create a proper user session with JWT token
        from ..auth import create_user_session
        token = create_user_session(user.id, user.email, user.name)

        return {
            "access_token": token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "email": user.email,
                "name": user.name
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Register error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")


@router.get("/me")
async def get_current_user_endpoint(current_user: AuthUser = Depends(require_auth())):
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


@router.post("/better-auth-callback")
async def better_auth_callback(request: Request):
    """
    Endpoint to handle callbacks from Better Auth.
    This is used when integrating with Better Auth to exchange tokens or sync user data.
    """
    try:
        # Get the raw request body
        body_bytes = await request.body()
        body_str = body_bytes.decode('utf-8')

        # Log the callback for debugging
        logger.info(f"Better Auth callback received: {body_str}")

        # Parse the body if it's JSON
        import json
        try:
            body_json = json.loads(body_str)
        except json.JSONDecodeError:
            body_json = {}

        # Respond appropriately based on the callback type
        callback_type = body_json.get('type', 'unknown')

        if callback_type == 'user-created':
            # Handle user creation callback
            logger.info("Processing user creation callback from Better Auth")
        elif callback_type == 'user-updated':
            # Handle user update callback
            logger.info("Processing user update callback from Better Auth")
        elif callback_type == 'session-created':
            # Handle session creation callback
            logger.info("Processing session creation callback from Better Auth")

        return {
            "status": "received",
            "callback_type": callback_type,
            "message": "Callback processed successfully"
        }
    except Exception as e:
        logger.error(f"Better Auth callback error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Callback processing failed: {str(e)}")