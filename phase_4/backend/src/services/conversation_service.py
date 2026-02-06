from sqlmodel import Session, select
from typing import List, Optional
from datetime import datetime
import uuid
from ..models.conversation import Conversation, ConversationCreate

class ConversationService:
    """Service class for handling conversation-related operations."""

    @staticmethod
    def create_conversation(session: Session, conversation_create: ConversationCreate) -> Conversation:
        """Create a new conversation."""
        conversation = Conversation(
            user_id=conversation_create.user_id
        )
        session.add(conversation)
        session.commit()
        session.refresh(conversation)
        return conversation

    @staticmethod
    def get_conversation_by_id(session: Session, conversation_id: uuid.UUID) -> Optional[Conversation]:
        """Get a conversation by its ID."""
        return session.get(Conversation, conversation_id)

    @staticmethod
    def get_conversations_by_user(session: Session, user_id: str) -> List[Conversation]:
        """Get all conversations for a specific user."""
        statement = select(Conversation).where(Conversation.user_id == user_id)
        return session.exec(statement).all()

    @staticmethod
    def update_conversation(session: Session, conversation_id: uuid.UUID) -> Optional[Conversation]:
        """Update a conversation's updated_at timestamp."""
        conversation = session.get(Conversation, conversation_id)
        if not conversation:
            return None

        conversation.updated_at = datetime.utcnow()
        session.add(conversation)
        session.commit()
        session.refresh(conversation)
        return conversation