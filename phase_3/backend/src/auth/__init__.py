"""
Authentication module for the AI-Powered Todo Chatbot.
Supports both custom JWT authentication and Better Auth JWT validation.
"""

from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
import os
from datetime import datetime, timedelta
import jwt
import requests
import bcrypt
from pydantic import BaseModel
from dotenv import load_dotenv
from sqlmodel import Session, select
from ..models.user import User, UserCreate

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


class LoginRequest(BaseModel):
    email: str
    password: str


class RegisterRequest(UserCreate):
    pass


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: User


def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password."""
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_custom_token(token: str) -> User:
    """Verify a custom JWT token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Create a user object
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


def verify_better_auth_token(token: str) -> User:
    """Verify a JWT token issued by Better Auth by calling the Better Auth server."""
    try:
        # Make a request to the Better Auth server to validate the token
        BETTER_AUTH_URL = os.getenv("BETTER_AUTH_URL", "http://localhost:3000")

        response = requests.get(
            f"{BETTER_AUTH_URL}/api/auth/session",
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            },
            timeout=10  # Add timeout to prevent hanging requests
        )

        if response.status_code == 200:
            session_data = response.json()
            user_data = session_data.get("user", {})

            user = User(
                id=user_data.get("id", ""),
                email=user_data.get("email", ""),
                name=user_data.get("name", "")
            )
            return user
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate Better Auth credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except requests.exceptions.RequestException as e:
        # Handle network-related errors specifically
        print(f"Network error verifying Better Auth token: {str(e)}")
        # If Better Auth server is not reachable, fall back to treating it as invalid token
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate Better Auth credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        # Handle any other errors (JSON parsing, etc.)
        print(f"Error verifying Better Auth token: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate Better Auth credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    """Get the current authenticated user, supporting both custom and Better Auth tokens."""
    token = credentials.credentials

    # First, try to verify as a custom JWT
    try:
        return verify_custom_token(token)
    except:
        # If that fails, try to verify as a Better Auth token
        try:
            return verify_better_auth_token(token)
        except:
            # If both fail, raise unauthorized error
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )


def require_auth():
    """Dependency to require authentication, supporting both custom and Better Auth tokens."""
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


def authenticate_user(email: str, password: str, session: Session) -> Optional[User]:
    """
    Authenticate a user by checking their credentials against the database.
    """
    statement = select(User).where(User.email == email)
    db_user = session.exec(statement).first()

    if db_user and verify_password(password, db_user.hashed_password):
        return User(
            id=db_user.id,
            email=db_user.email,
            name=db_user.name
        )
    return None


def register_user(user_data: UserCreate, session: Session) -> User:
    """
    Register a new user in the database.
    """
    # Check if user already exists
    statement = select(User).where(User.email == user_data.email)
    existing_user = session.exec(statement).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )

    # Hash the password
    hashed_password = hash_password(user_data.password)

    # Create new user
    db_user = User(
        email=user_data.email,
        name=user_data.name,
        hashed_password=hashed_password
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return User(
        id=db_user.id,
        email=db_user.email,
        name=db_user.name
    )