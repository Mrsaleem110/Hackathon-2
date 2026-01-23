from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import Dict, Any
from datetime import timedelta

from ..database.connection import get_session
from ..auth import (
    LoginRequest, RegisterRequest, TokenResponse,
    create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, User, get_current_user
)
from ..services.user_service import UserService

router = APIRouter(tags=["authentication"])


@router.post("/register", response_model=TokenResponse)
async def register(
    register_request: RegisterRequest,
    session: Session = Depends(get_session)
):
    """
    Register a new user and return an access token.
    """
    try:
        # Check if user already exists
        existing_user = UserService.get_user_by_email(register_request.email, session)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists"
            )

        # Register the user
        user = UserService.create_user(register_request, session)

        # Create access token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.id, "email": user.email, "name": user.name},
            expires_delta=access_token_expires
        )

        # Convert to auth.User model for response
        return_user = User(id=user.id, email=user.email, name=user.name)

        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            user=return_user
        )
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}"
        )


@router.post("/login", response_model=TokenResponse)
async def login(
    login_request: LoginRequest,
    session: Session = Depends(get_session)
):
    """
    Authenticate user and return an access token.
    """
    user = UserService.authenticate_user(login_request.email, login_request.password, session)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.id, "email": user.email, "name": user.name},
        expires_delta=access_token_expires
    )

    # Convert to auth.User model for response
    return_user = User(id=user.id, email=user.email, name=user.name)

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user=return_user
    )


@router.post("/refresh")
async def refresh_token(
    current_user: User = Depends(get_current_user)
):
    """
    Refresh the access token.
    """
    # Create a new access token for the current user
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": current_user.id, "email": current_user.email, "name": current_user.name},
        expires_delta=access_token_expires
    )

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user=current_user
    )


@router.get("/me", response_model=User)
async def get_current_user_profile(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get the profile of the currently authenticated user.
    """
    # Fetch the user from the database to ensure we have the latest data
    db_user = UserService.get_user_by_id(current_user.id, session)

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Return the user information
    return User(id=db_user.id, email=db_user.email, name=db_user.name)