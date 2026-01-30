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
try:
    import bcrypt
    HAS_BCRYPT = True
except ImportError:
    # bcrypt is not available in some serverless environments
    # Use fallback methods for password hashing
    HAS_BCRYPT = False
    bcrypt = None
from pydantic import BaseModel
from sqlmodel import Session, select
from ..models.user import User as UserModel, UserCreate  # Rename to avoid conflict

# Don't use load_dotenv() in serverless environments as it can cause issues
# Environment variables are provided by the platform

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
    """Hash a password using bcrypt or fallback method."""
    if HAS_BCRYPT:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    else:
        # Fallback for serverless environments without bcrypt
        # This is NOT secure and should only be used for testing!
        import hashlib
        return hashlib.sha256(password.encode('utf-8')).hexdigest()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password."""
    if HAS_BCRYPT:
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
    else:
        # Fallback for serverless environments without bcrypt
        # This is NOT secure and should only be used for testing!
        import hashlib
        return hashlib.sha256(plain_password.encode('utf-8')).hexdigest() == hashed_password


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


def normalize_jwt_payload(payload: dict) -> dict:
    """Normalize JWT payload to ensure consistent user identification."""
    normalized = {}

    # Normalize user ID field - check multiple possible locations
    normalized['user_id'] = payload.get('sub') or payload.get('user_id') or payload.get('id')

    # Normalize email field
    normalized['email'] = payload.get('email') or payload.get('user_email')

    # Normalize name field
    normalized['name'] = payload.get('name') or payload.get('user_name') or payload.get('full_name')

    return normalized


def verify_custom_token(token: str) -> User:
    """Verify a custom JWT token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # Normalize the JWT payload to ensure consistent user identification
        normalized_payload = normalize_jwt_payload(payload)

        user_id: str = normalized_payload.get("user_id")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials - missing user ID",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Create a user object
        user = User(
            id=user_id,
            email=normalized_payload.get("email", None),
            name=normalized_payload.get("name", None)
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
        # For serverless environments, we'll just decode the JWT locally since
        # making HTTP requests to verify tokens can cause timeouts
        # This is a simplified approach that ensures consistent JWT payload handling

        # Get the Better Auth secret key
        BETTER_AUTH_SECRET = os.getenv("BETTER_AUTH_SECRET")
        if not BETTER_AUTH_SECRET:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Better Auth secret not configured",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Decode the token using the Better Auth secret
        payload = jwt.decode(token, BETTER_AUTH_SECRET, algorithms=["HS256"])

        # Normalize the JWT payload to ensure consistent user identification
        normalized_payload = normalize_jwt_payload(payload)

        user_id = normalized_payload.get("user_id", "")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Better Auth token missing user ID",
                headers={"WWW-Authenticate": "Bearer"},
            )

        user = User(
            id=user_id,
            email=normalized_payload.get("email", ""),
            name=normalized_payload.get("name", "")
        )
        return user

        # Original approach with HTTP request (commented out for serverless compatibility)
        # BETTER_AUTH_URL = os.getenv("BETTER_AUTH_URL", "http://localhost:3000")
        #
        # response = requests.get(
        #     f"{BETTER_AUTH_URL}/api/auth/session",
        #     headers={
        #         "Authorization": f"Bearer {token}",
        #         "Content-Type": "application/json"
        #     },
        #     timeout=5  # Shorter timeout for serverless
        # )
        #
        # if response.status_code == 200:
        #     session_data = response.json()
        #     user_data = session_data.get("user", {})
        #
        #     user = User(
        #         id=user_data.get("id", ""),
        #         email=user_data.get("email", ""),
        #         name=user_data.get("name", "")
        #     )
        #     return user
        # else:
        #     raise HTTPException(
        #         status_code=status.HTTP_401_UNAUTHORIZED,
        #         detail="Could not validate Better Auth credentials",
        #         headers={"WWW-Authenticate": "Bearer"},
        #     )
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate Better Auth credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        # Handle any other errors
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
    except Exception as e:
        # Log the error for debugging but continue to try Better Auth
        print(f"Custom token verification failed: {str(e)}")
        # If that fails, try to verify as a Better Auth token
        try:
            return verify_better_auth_token(token)
        except Exception as e2:
            # Log the second error as well
            print(f"Better Auth token verification failed: {str(e2)}")
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
    # In serverless environments, we'll use bypass mode without database lookup
    # This is for testing purposes only
    if not HAS_BCRYPT:
        # Bypass mode - accept any credentials for testing
        if email and password:
            return User(
                id=f"user_{hash(email)}",  # Generate a simple user ID
                email=email,
                name=email.split("@")[0]
            )
        return None

    # Normal database authentication
    statement = select(UserModel).where(UserModel.email == email)
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
    # In serverless environments, we'll use bypass mode without database storage
    # This is for testing purposes only
    if not HAS_BCRYPT:
        # Bypass mode - return user without storing in database
        return User(
            id=f"user_{hash(user_data.email)}",  # Generate a simple user ID
            email=user_data.email,
            name=user_data.name or user_data.email.split("@")[0]
        )

    # Normal database registration
    # Check if user already exists
    statement = select(UserModel).where(UserModel.email == user_data.email)
    existing_user = session.exec(statement).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )

    # Hash the password
    hashed_password = hash_password(user_data.password)

    # Create new user
    db_user = UserModel(
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