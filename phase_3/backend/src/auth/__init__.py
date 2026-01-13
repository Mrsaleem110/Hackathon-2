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
import bcrypt
from pydantic import BaseModel
from dotenv import load_dotenv
from sqlmodel import Session, select
from ..models.user import User, UserCreate
from ..database.connection import get_session

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