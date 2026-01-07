"""
Authentication module for the AI-Powered Todo Chatbot.
Better Auth is a JavaScript library, so for Python we're implementing a similar interface
using standard JWT authentication with additional security features.
"""
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
import os
from datetime import datetime, timedelta
import jwt
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Secret key for JWT (in production, this should be a strong secret)
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET", "your-default-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

security = HTTPBearer()

class User(BaseModel):
    id: str
    email: Optional[str] = None
    name: Optional[str] = None

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a JWT access token similar to Better Auth."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> User:
    """Verify a JWT token and return the user info."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Create a user object similar to what Better Auth would provide
        user = User(
            id=user_id,
            email=payload.get("email", None),
            name=payload.get("name", None)
        )
        return user
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    """Get the current authenticated user, similar to Better Auth's interface."""
    token = credentials.credentials
    return verify_token(token)

def require_auth():
    """Dependency to require authentication."""
    def auth_dependency(request: Request = None, current_user: User = Depends(get_current_user)):
        return current_user
    return auth_dependency

def create_user_session(user_id: str, email: str = None, name: str = None) -> str:
    """Create an authentication session for a user, similar to Better Auth."""
    data = {"sub": user_id}
    if email:
        data["email"] = email
    if name:
        data["name"] = name

    token = create_access_token(data=data)
    return token

def authenticate_user(user_id: str, password: str) -> Optional[User]:
    """
    Authenticate a user.
    In a real implementation, this would check against a user database.
    For this implementation, we'll just verify the user_id exists.
    """
    # In a real implementation, this would check the user's credentials
    # against a database, similar to how Better Auth would work
    if user_id is not None and len(user_id) > 0:
        return User(id=user_id)
    return None