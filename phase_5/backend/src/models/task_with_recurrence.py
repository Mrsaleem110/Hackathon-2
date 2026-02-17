from sqlmodel import SQLModel, Field
from typing import Optional, List, Dict, Any
import uuid
from datetime import datetime

class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = None
    status: str = Field(default="active")
    priority: str = Field(default="medium")
    due_date: Optional[datetime] = None
    reminder_time: Optional[datetime] = None
    recurrence_pattern: Optional[Dict[str, Any]] = None
    tags: Optional[List[str]] = []
    user_id: str

class Task(TaskBase, table=True):
    __tablename__ = "tasks"

    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    parent_task_id: Optional[uuid.UUID] = None

class TaskCreate(TaskBase):
    pass

class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    due_date: Optional[datetime] = None
    reminder_time: Optional[datetime] = None
    recurrence_pattern: Optional[Dict[str, Any]] = None
    tags: Optional[List[str]] = None
    completed_at: Optional[datetime] = None