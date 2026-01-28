from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Optional, Dict, Any
import os
import openai
from datetime import datetime, timedelta
import jwt
import time
import uuid

from ..auth import require_auth, User

router = APIRouter()

# Configuration - In a real app, these would come from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable is required")

# Set the OpenAI API key
openai.api_key = OPENAI_API_KEY

class ChatKitSessionRequest(BaseModel):
    workflow_id: str
    user_id: str
    metadata: Optional[Dict[str, Any]] = None


class ChatKitSessionResponse(BaseModel):
    client_secret: str
    session_id: str
    workflow_id: str
    user_id: str
    expires_at: datetime
    metadata: Optional[Dict[str, Any]] = None


@router.post("/chatkit/session", response_model=ChatKitSessionResponse)
async def create_chatkit_session(
    request: ChatKitSessionRequest,
    current_user: User = Depends(require_auth())
):
    """
    Create a new ChatKit session using OpenAI's API
    This endpoint generates a client_secret that can be used by the frontend
    to connect to the OpenAI-hosted ChatKit UI.
    """
    try:
        # In a real implementation, this would call the OpenAI ChatKit sessions API
        # For now, we'll simulate the process by generating a JWT token
        # that represents the client_secret

        session_id = str(uuid.uuid4())

        # Create payload for the client secret JWT
        payload = {
            "session_id": session_id,
            "user_id": request.user_id,
            "workflow_id": request.workflow_id,
            "iat": int(time.time()),
            "exp": int(time.time()) + (60 * 60),  # 1 hour expiry
            "iss": "openai-chatkit-agent",
            "sub": f"session:{session_id}",
            "permissions": ["read", "write"]  # Basic permissions
        }

        # Add any additional metadata
        if request.metadata:
            payload.update(request.metadata)

        # Sign the JWT with a secret (in production, this should be a proper secret)
        client_secret = jwt.encode(
            payload,
            os.getenv("CHATKIT_SECRET", "your-secret-key-here"),
            algorithm="HS256"
        )

        response = ChatKitSessionResponse(
            client_secret=client_secret,
            session_id=session_id,
            workflow_id=request.workflow_id,
            user_id=request.user_id,
            expires_at=datetime.utcnow() + timedelta(hours=1),
            metadata=request.metadata
        )

        return response

    except openai.APIError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"OpenAI API error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create ChatKit session: {str(e)}"
        )


@router.post("/chatkit/session/{session_id}/refresh")
async def refresh_chatkit_session(
    session_id: str,
    current_user: User = Depends(require_auth())
):
    """
    Refresh an existing ChatKit session by generating a new client_secret
    """
    try:
        # In a real implementation, this would refresh the session with OpenAI
        # For now, we'll generate a new token with extended expiration

        payload = {
            "session_id": session_id,
            "user_id": current_user.id,
            "iat": int(time.time()),
            "exp": int(time.time()) + (60 * 60),  # 1 hour expiry
            "iss": "openai-chatkit-agent",
            "sub": f"session:{session_id}",
            "permissions": ["read", "write"]
        }

        new_client_secret = jwt.encode(
            payload,
            os.getenv("CHATKIT_SECRET", "your-secret-key-here"),
            algorithm="HS256"
        )

        return {
            "client_secret": new_client_secret,
            "session_id": session_id,
            "expires_at": datetime.utcnow() + timedelta(hours=1)
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to refresh ChatKit session: {str(e)}"
        )


@router.get("/chatkit/workflow/{workflow_id}")
async def get_workflow_details(
    workflow_id: str,
    current_user: User = Depends(require_auth())
):
    """
    Get details about a specific workflow
    In a real implementation, this would fetch from OpenAI's API
    """
    try:
        # This is a mock implementation
        # In a real implementation, you would call OpenAI's API to get workflow details
        return {
            "workflow_id": workflow_id,
            "name": f"Workflow {workflow_id}",
            "description": "OpenAI-hosted agent workflow",
            "status": "active",
            "capabilities": ["text-generation", "function-calling", "file-processing"],
            "created_at": datetime.utcnow(),
            "user_access": current_user.id
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get workflow details: {str(e)}"
        )


# Note: The actual OpenAI ChatKit API might have different endpoints
# This is a representation based on the specification provided