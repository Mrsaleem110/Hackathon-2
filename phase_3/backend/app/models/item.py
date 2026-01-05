from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime
from .user import User
from enum import Enum


class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class ItemBase(SQLModel):
    title: str
    description: str
    completed: bool = False
    priority: Optional[Priority] = Priority.MEDIUM
    category: Optional[str] = None
    due_date: Optional[datetime] = None
    recurring: Optional[str] = None  # e.g., "daily", "weekly", "monthly"


class Item(ItemBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    owner_id: int = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to owner - using string reference to avoid circular import
    owner: "User" = Relationship(back_populates="items")


class ItemCreate(ItemBase):
    pass


class ItemRead(ItemBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime


class ItemUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[Priority] = None
    category: Optional[str] = None
    due_date: Optional[datetime] = None
    recurring: Optional[str] = None