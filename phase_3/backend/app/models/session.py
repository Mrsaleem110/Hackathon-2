from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime
from .user import User


class SessionBase(SQLModel):
    token: str = Field(unique=True, nullable=False)
    expires_at: datetime


class Session(SessionBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to user - using string reference to avoid circular import
    user: "User" = Relationship(back_populates="sessions")


class SessionCreate(SessionBase):
    user_id: int


class SessionRead(SessionBase):
    id: int
    user_id: int
    created_at: datetime