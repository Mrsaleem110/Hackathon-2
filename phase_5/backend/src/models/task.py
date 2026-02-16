from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid
from enum import Enum
from sqlalchemy import Column, ForeignKey

class PriorityEnum(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"

class TaskBase(SQLModel):
    title: str
    description: Optional[str] = None
    completed: bool = False
    user_id: str = Field(sa_column=Column(ForeignKey("user.id")))
    priority: str = Field(default="medium")  # Default to medium priority
    due_date: Optional[str] = Field(default=None)  # Due date in YYYY-MM-DD format

class Task(TaskBase, table=True):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[str] = None
    due_date: Optional[str] = None

class TaskCreateRequest(SQLModel):
    """Request model for creating a task - user_id comes from auth, not from request"""
    title: str
    description: Optional[str] = None
    completed: bool = False
    priority: str = "medium"
    due_date: Optional[str] = None

class TaskCreate(TaskBase):
    pass