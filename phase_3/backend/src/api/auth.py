from fastapi import APIRouter, Depends, HTTPException, status, Body
from pydantic import BaseModel
import logging
import traceback

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

# Test endpoint to verify router is registered
@router.get("/test")
async def test_auth_endpoint():
    """Test endpoint to verify auth router is working"""
    diagnostics = {}
    
    # Test each import
    try:
        from sqlmodel import Session
        diagnostics["sqlmodel"] = "✓"
    except Exception as e:
        diagnostics["sqlmodel"] = f"✗ {str(e)}"
    
    try:
        from ..database.connection import DATABASE_URL
        diagnostics["database_url"] = "✓" if DATABASE_URL else "✗ No URL"
    except Exception as e:
        diagnostics["database_url"] = f"✗ {str(e)}"
    
    try:
        from ..auth import LoginRequest, RegisterRequest, TokenResponse
        diagnostics["auth_models"] = "✓"
    except Exception as e:
        diagnostics["auth_models"] = f"✗ {str(e)}"
    
    try:
        from ..services.user_service import UserService
        diagnostics["user_service"] = "✓"
    except Exception as e:
        diagnostics["user_service"] = f"✗ {str(e)}"
    
    return {"status": "online", "diagnostics": diagnostics}


@router.post("/login")
async def login(credentials: LoginRequestModel):
    """Login endpoint"""
    try:
        logger.info(f"Login attempt for: {credentials.email}")
        
        from ..services.user_service import UserService
        from ..database.connection import DATABASE_URL
        from ..auth import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
        from datetime import timedelta
        from sqlmodel import Session, create_engine
        
        # Create engine and session
        engine = create_engine(DATABASE_URL, echo=False, connect_args={"sslmode": "require"} if "neon" in DATABASE_URL.lower() else {})
        session = Session(engine)
        
        try:
            # Authenticate user
            user = UserService.authenticate_user(credentials.email, credentials.password, session)
            
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid email or password"
                )
            
            # Create token
            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = create_access_token(
                data={"sub": user.id, "email": user.email, "name": user.name},
                expires_delta=access_token_expires
            )
            
            return {
                "access_token": access_token,
                "token_type": "bearer",
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "name": user.name
                }
            }
        finally:
            session.close()
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Login failed: {str(e)}")


@router.post("/register")
async def register(credentials: RegisterRequestModel):
    """Register endpoint"""
    try:
        logger.info(f"Register attempt for: {credentials.email}")
        
        from ..services.user_service import UserService
        from ..database.connection import DATABASE_URL
        from ..auth import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, RegisterRequest
        from datetime import timedelta
        from sqlmodel import Session, create_engine
        
        # Create engine and session
        engine = create_engine(DATABASE_URL, echo=False, connect_args={"sslmode": "require"} if "neon" in DATABASE_URL.lower() else {})
        session = Session(engine)
        
        try:
            # Check if user exists
            existing_user = UserService.get_user_by_email(credentials.email, session)
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="User already exists"
                )
            
            # Create user
            user_data = RegisterRequest(
                email=credentials.email, 
                password=credentials.password, 
                name=credentials.name or credentials.email
            )
            user = UserService.create_user(user_data, session)
            
            # Create token
            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = create_access_token(
                data={"sub": user.id, "email": user.email, "name": user.name},
                expires_delta=access_token_expires
            )
            
            return {
                "access_token": access_token,
                "token_type": "bearer",
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "name": user.name
                }
            }
        finally:
            session.close()
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Register error: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")