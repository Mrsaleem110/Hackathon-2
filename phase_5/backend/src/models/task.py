from sqlmodel import SQLModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
import uuid
from sqlalchemy import Column, Text, JSON

class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(sa_column=Column(Text))
    status: str = Field(default="active")
    priority: str = Field(default="medium")
    recurrence_pattern: Optional[Dict[str, Any]] = Field(default=None, sa_column=Column(JSON))
    tags: Optional[List[str]] = []
    user_id: str

class TaskUpdate(SQLModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    due_date: Optional[datetime] = None
    reminder_time: Optional[datetime] = None
    recurrence_pattern: Optional[dict] = Field(default=None, sa_column=Column(JSON))
    tags: Optional[List[str]] = None

class TaskCreateRequest(SQLModel):
    """Request model for creating a task - user_id comes from auth, not from request"""
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = None
    priority: str = "medium"
    due_date: Optional[datetime] = None
    reminder_time: Optional[datetime] = None
    recurrence_pattern: Optional[dict] = Field(default=None, sa_column=Column(JSON))
    tags: Optional[List[str]] = []

class TaskCreate(TaskBase):
    pass