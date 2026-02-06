from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import jwt
import json
import uuid
import time
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
import os

from ..auth import get_current_user, require_auth, User

router = APIRouter()

# Configuration - In a real app, these would come from environment variables
CHATKIT_SECRET = os.getenv("CHATKIT_SECRET", "your-secret-key-here")
SESSION_EXPIRY_MINUTES = 60  # Session expires after 1 hour


class SessionRequest(BaseModel):
    userId: str
    workflowId: str
    metadata: Optional[dict] = None


class SessionResponse(BaseModel):
    session_token: str
    session_id: str
    user_id: str
    workflow_id: str
    expires_at: datetime
    metadata: Optional[dict] = None


class RefreshRequest(BaseModel):
    sessionId: str


# OpenAI ChatKit session management endpoints
@router.post("/chatkit/session", response_model=SessionResponse)
async def create_chatkit_session(request: SessionRequest):
    """
    Create a new OpenAI ChatKit session with a signed JWT token
    """
    try:
        # Generate a unique session ID
        session_id = str(uuid.uuid4())

        # Create payload for JWT token
        payload = {
            "session_id": session_id,
            "user_id": request.userId,
            "workflow_id": request.workflowId,
            "iat": int(time.time()),
            "exp": int(time.time()) + (SESSION_EXPIRY_MINUTES * 60),
            "iss": "chatkit-backend",
            "sub": f"session:{session_id}"
        }

        # Add any additional metadata
        if request.metadata:
            payload.update(request.metadata)

        # Sign the JWT with the secret
        session_token = jwt.encode(payload, CHATKIT_SECRET, algorithm="HS256")

        response = SessionResponse(
            session_token=session_token,
            session_id=session_id,
            user_id=request.userId,
            workflow_id=request.workflowId,
            expires_at=datetime.utcnow() + timedelta(minutes=SESSION_EXPIRY_MINUTES),
            metadata=request.metadata
        )

        return response

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create ChatKit session: {str(e)}"
        )


@router.post("/chatkit/session/{session_id}/refresh", response_model=SessionResponse)
async def refresh_chatkit_session(session_id: str):
    """
    Refresh an existing ChatKit session by generating a new token
    """
    try:
        # Create a new token with extended expiration
        payload = {
            "session_id": session_id,
            "iat": int(time.time()),
            "exp": int(time.time()) + (SESSION_EXPIRY_MINUTES * 60),
            "iss": "chatkit-backend",
            "sub": f"session:{session_id}"
        }

        new_session_token = jwt.encode(payload, CHATKIT_SECRET, algorithm="HS256")

        # For demo purposes, we'll return basic session info
        # In a real implementation, you'd retrieve the original session details
        response = SessionResponse(
            session_token=new_session_token,
            session_id=session_id,
            user_id="unknown_user",  # Would come from stored session data
            workflow_id="unknown_workflow",  # Would come from stored session data
            expires_at=datetime.utcnow() + timedelta(minutes=SESSION_EXPIRY_MINUTES)
        )

        return response

    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid session token")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to refresh ChatKit session: {str(e)}"
        )


@router.get("/chatkit/session/{session_id}/validate")
async def validate_chatkit_session(session_id: str):
    """
    Validate if a ChatKit session is still active
    """
    try:
        # In a real implementation, you'd check if the session exists in a database/cache
        # For demo, we'll just return a mock response indicating validity

        return {
            "valid": True,
            "session_id": session_id,
            "expires_at": datetime.utcnow() + timedelta(minutes=SESSION_EXPIRY_MINUTES)
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to validate ChatKit session: {str(e)}"
        )


# Additional endpoint to get workflow configuration
@router.get("/chatkit/workflows/{workflow_id}")
async def get_workflow_config(workflow_id: str, current_user: User = Depends(require_auth())):
    """
    Get configuration for a specific workflow
    """
    # In a real implementation, this would fetch from a database or OpenAI API
    # For demo purposes, return a basic configuration
    return {
        "workflow_id": workflow_id,
        "name": f"Workflow {workflow_id}",
        "description": "OpenAI-hosted agent workflow",
        "capabilities": ["text-generation", "function-calling", "file-processing"],
        "user_access": current_user.id if current_user else "anonymous"
    }


# Legacy endpoint for backward compatibility
@router.get("/chatkit/token")
async def get_legacy_chatkit_token(current_user: User = Depends(require_auth())):
    """
    Legacy endpoint for backward compatibility.
    Generate a token for Chatkit authentication.
    This is a simplified implementation - in a real scenario, you'd use the official Chatkit server library.
    """
    try:
        # In a real implementation, you would generate a Chatkit token using the official library
        # For now, returning a mock response to satisfy the frontend requirement
        return JSONResponse(
            status_code=200,
            content={
                "token": "mock-chatkit-token-for-demo",
                "user_id": current_user.id if current_user else "demo-user",
                "expires_in": 3600  # Token expires in 1 hour
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating Chatkit token: {str(e)}"
        )