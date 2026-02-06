from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime
import uuid
from enum import Enum
from sqlalchemy import Column, ForeignKey

class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"

class MessageBase(SQLModel):
    conversation_id: uuid.UUID = Field(sa_column=Column(ForeignKey("conversation.id")))
    user_id: str
    role: MessageRole
    content: str

class Message(MessageBase, table=True):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to conversation
    conversation: Optional["Conversation"] = Relationship(back_populates="messages")

class MessageCreate(MessageBase):
    pass