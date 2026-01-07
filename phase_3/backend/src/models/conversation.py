from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
import uuid

class ConversationBase(SQLModel):
    user_id: str

class Conversation(ConversationBase, table=True):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default=datetime.utcnow())
    updated_at: datetime = Field(default=datetime.utcnow())

    # Relationship to messages
    messages: List["Message"] = Relationship(back_populates="conversation")

class ConversationCreate(ConversationBase):
    pass