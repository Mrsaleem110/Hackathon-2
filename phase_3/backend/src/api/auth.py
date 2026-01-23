from fastapi import APIRouter, Depends, HTTPException, status
import logging
import traceback

logger = logging.getLogger(__name__)

router = APIRouter(tags=["authentication"])

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
        from ..database.connection import get_session
        diagnostics["database"] = "✓"
    except Exception as e:
        diagnostics["database"] = f"✗ {str(e)}"
    
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
    
    return diagnostics


# Simple working endpoints first
@router.post("/login")
async def login(request: dict = None):
    """Test login endpoint"""
    try:
        logger.info(f"Login attempt with request: {request}")
        
        if not request:
            raise HTTPException(status_code=400, detail="Request body required")
        
        email = request.get("email")
        password = request.get("password")
        
        if not email or not password:
            raise HTTPException(status_code=400, detail="Email and password required")
        
        # Try to authenticate
        from ..services.user_service import UserService
        from ..database.connection import get_session
        from ..auth import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, User, TokenResponse
        from datetime import timedelta
        
        # Get session
        from sqlmodel import Session, create_engine, SQLModel
        from ..database.connection import DATABASE_URL
        engine = create_engine(DATABASE_URL, echo=False)
        session = Session(engine)
        
        try:
            user = UserService.authenticate_user(email, password, session)
            
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid email or password"
                )
            
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
async def register(request: dict = None):
    """Test register endpoint"""
    try:
        logger.info(f"Register attempt with request: {request}")
        
        if not request:
            raise HTTPException(status_code=400, detail="Request body required")
        
        email = request.get("email")
        password = request.get("password")
        name = request.get("name")
        
        if not email or not password:
            raise HTTPException(status_code=400, detail="Email and password required")
        
        from ..services.user_service import UserService
        from ..database.connection import get_session
        from ..auth import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, User, TokenResponse, RegisterRequest
        from datetime import timedelta
        
        # Get session
        from sqlmodel import Session, create_engine
        from ..database.connection import DATABASE_URL
        engine = create_engine(DATABASE_URL, echo=False)
        session = Session(engine)
        
        try:
            # Check if user exists
            existing_user = UserService.get_user_by_email(email, session)
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="User already exists"
                )
            
            # Create user
            user_data = RegisterRequest(email=email, password=password, name=name or email)
            user = UserService.create_user(user_data, session)
            
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