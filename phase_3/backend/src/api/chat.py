from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import Dict, Any, List, Optional
import uuid
from datetime import datetime

from ..database.connection import get_session
from ..models.conversation import Conversation
from ..models.message import Message, MessageCreate, MessageRole
from ..models.task import Task
from ..services.conversation_service import ConversationService
from ..services.message_service import MessageService
from ..agents.chat_agent import ChatAgent
from ..auth import get_current_user, require_auth, User

router = APIRouter()

@router.post("/api/{user_id}/chat")
async def chat_endpoint(
    user_id: str,
    request: Dict[str, Any],
    current_user: User = Depends(require_auth()),
    session: Session = Depends(get_session)
):
    """
    Process a chat message and return AI response with tool calls.
    """
    try:
        # Ensure the authenticated user matches the user_id in the path
        if current_user.id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied: You can only access your own conversations"
            )

        # Extract message and conversation_id from request
        message_content = request.get("message")
        if not message_content:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Message content is required"
            )

        conversation_id_str = request.get("conversation_id")
        conversation_id = None
        if conversation_id_str:
            try:
                conversation_id = uuid.UUID(conversation_id_str)
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid conversation_id format"
                )

        # Get or create conversation
        if conversation_id:
            conversation = session.get(Conversation, conversation_id)
            if not conversation:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Conversation not found"
                )
            if conversation.user_id != user_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Access denied to this conversation"
                )
        else:
            # Create new conversation
            conversation_create = Conversation(user_id=user_id)
            conversation = ConversationService.create_conversation(session, conversation_create)
            conversation_id = conversation.id

        # Create user message
        user_message = MessageCreate(
            conversation_id=conversation_id,
            user_id=user_id,
            role=MessageRole.USER,
            content=message_content
        )
        MessageService.create_message(session, user_message)

        # Get recent conversation history for context
        recent_messages = MessageService.get_recent_messages_by_conversation(session, conversation_id, limit=10)
        conversation_history = []
        for msg in recent_messages:
            conversation_history.append({
                "role": msg.role.value,
                "content": msg.content
            })

        # Process message with AI agent
        agent = ChatAgent()
        result = agent.process_message(message_content, user_id, conversation_history)

        # Create assistant message with the AI response
        assistant_message = MessageCreate(
            conversation_id=conversation_id,
            user_id=user_id,  # The AI acts on behalf of the system/user
            role=MessageRole.ASSISTANT,
            content=result["response"]
        )
        MessageService.create_message(session, assistant_message)

        # Update conversation timestamp
        ConversationService.update_conversation(session, conversation_id)

        # Return the response with conversation_id and tool calls
        return {
            "conversation_id": str(conversation_id),
            "response": result["response"],
            "tool_calls": result["tool_calls"]
        }

    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Handle any other exceptions
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )