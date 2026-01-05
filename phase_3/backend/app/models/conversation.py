from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
import uuid
from sqlalchemy import JSON


class Conversation(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    user_id: str = Field(index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship with messages
    messages: List["Message"] = Relationship(back_populates="conversation")


class Message(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    conversation_id: str = Field(foreign_key="conversation.id", index=True)
    role: str = Field(index=True)  # 'user', 'assistant', 'system'
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    extra_data: Optional[dict] = Field(default={}, sa_type=JSON)  # Changed from 'metadata' to avoid conflict

    # Relationship with conversation
    conversation: Conversation = Relationship(back_populates="messages")