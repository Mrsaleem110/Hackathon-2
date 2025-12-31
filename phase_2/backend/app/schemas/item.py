from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum


class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class ItemBase(BaseModel):
    title: str
    description: str
    completed: bool = False
    priority: Optional[Priority] = Priority.MEDIUM
    category: Optional[str] = None
    due_date: Optional[datetime] = None
    recurring: Optional[str] = None  # e.g., "daily", "weekly", "monthly"


class ItemCreate(ItemBase):
    pass


class ItemRead(ItemBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime


class ItemUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[Priority] = None
    category: Optional[str] = None
    due_date: Optional[datetime] = None
    recurring: Optional[str] = None


class ItemWithOwner(ItemRead):
    owner: 'UserRead'