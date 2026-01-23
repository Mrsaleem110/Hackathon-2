from fastapi import APIRouter, Depends, HTTPException, status, Body
from pydantic import BaseModel
import logging
import traceback
import os

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

# DIAGNOSTIC ENDPOINT
@router.get("/test")
async def test_auth_endpoint():
    """Test endpoint to verify auth router and database connection"""
    diagnostics = {
        "status": "testing",
        "environment": os.getenv("VERCEL_ENV", "local"),
        "checks": {}
    }
    
    # Check database URL
    try:
        from ..database.connection import DATABASE_URL
        diagnostics["checks"]["database_url"] = "✓ Available" if DATABASE_URL else "✗ Missing"
        diagnostics["database_configured"] = bool(DATABASE_URL)
    except Exception as e:
        diagnostics["checks"]["database_url"] = f"✗ {str(e)}"
        diagnostics["database_configured"] = False
    
    # Try to connect to database
    try:
        from sqlmodel import create_engine, Session, select, SQLModel
        from ..database.connection import DATABASE_URL
        
        connect_args = {}
        if DATABASE_URL and "neon" in DATABASE_URL.lower():
            connect_args = {"sslmode": "require"}
        
        engine = create_engine(DATABASE_URL, echo=False, connect_args=connect_args)
        test_session = Session(engine)
        
        # Try a simple query
        result = test_session.exec(select(1)).first()
        test_session.close()
        
        diagnostics["checks"]["database_connection"] = "✓ Connected"
        diagnostics["db_connected"] = True
    except Exception as e:
        diagnostics["checks"]["database_connection"] = f"✗ {str(e)}"
        diagnostics["db_connected"] = False
    
    # Check if User table exists
    try:
        from ..models.user import User as UserModel
        from sqlmodel import create_engine, Session, inspect
        from ..database.connection import DATABASE_URL
        
        connect_args = {}
        if DATABASE_URL and "neon" in DATABASE_URL.lower():
            connect_args = {"sslmode": "require"}
        
        engine = create_engine(DATABASE_URL, echo=False, connect_args=connect_args)
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        user_table_exists = "user" in tables
        diagnostics["checks"]["user_table"] = "✓ Exists" if user_table_exists else "✗ Missing"
        diagnostics["user_table_exists"] = user_table_exists
        diagnostics["available_tables"] = tables
        
    except Exception as e:
        diagnostics["checks"]["user_table"] = f"✗ {str(e)}"
        diagnostics["user_table_exists"] = False
    
    return diagnostics


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
        
        if not DATABASE_URL:
            raise HTTPException(status_code=503, detail="Database not configured")
        
        # Create engine with SSL support for NeonDB
        connect_args = {}
        if "neon" in DATABASE_URL.lower():
            connect_args = {"sslmode": "require"}
        
        try:
            engine = create_engine(
                DATABASE_URL, 
                echo=False,
                pool_pre_ping=True,
                connect_args=connect_args
            )
        except Exception as e:
            logger.error(f"Failed to create engine: {str(e)}")
            raise HTTPException(status_code=503, detail=f"Database error: {str(e)}")
        
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
        logger.error(f"Traceback: {traceback.format_exc()}")
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
        
        if not DATABASE_URL:
            raise HTTPException(status_code=503, detail="Database not configured")
        
        # Create engine with SSL support for NeonDB
        connect_args = {}
        if "neon" in DATABASE_URL.lower():
            connect_args = {"sslmode": "require"}
        
        try:
            engine = create_engine(
                DATABASE_URL,
                echo=False,
                pool_pre_ping=True,
                connect_args=connect_args
            )
        except Exception as e:
            logger.error(f"Failed to create engine: {str(e)}")
            raise HTTPException(status_code=503, detail=f"Database error: {str(e)}")
        
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
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")