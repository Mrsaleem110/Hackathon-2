from sqlmodel import Session, select
from typing import List, Optional
from datetime import datetime
import uuid
from ..models.message import Message, MessageCreate, MessageRole

class MessageService:
    """Service class for handling message-related operations."""

    @staticmethod
    def create_message(session: Session, message_create: MessageCreate) -> Message:
        """Create a new message."""
        message = Message(
            conversation_id=message_create.conversation_id,
            user_id=message_create.user_id,
            role=message_create.role,
            content=message_create.content
        )
        session.add(message)
        session.commit()
        session.refresh(message)
        return message

    @staticmethod
    def get_message_by_id(session: Session, message_id: uuid.UUID) -> Optional[Message]:
        """Get a message by its ID."""
        return session.get(Message, message_id)

    @staticmethod
    def get_messages_by_conversation(session: Session, conversation_id: uuid.UUID) -> List[Message]:
        """Get all messages for a specific conversation."""
        statement = select(Message).where(Message.conversation_id == conversation_id).order_by(Message.created_at)
        return session.exec(statement).all()

    @staticmethod
    def get_messages_by_user(session: Session, user_id: str) -> List[Message]:
        """Get all messages for a specific user."""
        statement = select(Message).where(Message.user_id == user_id).order_by(Message.created_at)
        return session.exec(statement).all()

    @staticmethod
    def get_recent_messages_by_conversation(session: Session, conversation_id: uuid.UUID, limit: int = 10) -> List[Message]:
        """Get recent messages for a specific conversation."""
        statement = select(Message).where(Message.conversation_id == conversation_id).order_by(Message.created_at.desc()).limit(limit)
        messages = session.exec(statement).all()
        # Reverse to return in chronological order
        return list(reversed(messages))