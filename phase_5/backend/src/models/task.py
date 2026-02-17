from sqlmodel import SQLModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
import uuid
from sqlalchemy import Column, Text, JSON


class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(sa_column=Column(Text))
    status: str = Field(default="active")
    priority: str = Field(default="medium")  # Can be "high", "medium", or "low"
    due_date: Optional[datetime] = None
    reminder_time: Optional[datetime] = None
    recurrence_pattern: Optional[Dict[str, Any]] = Field(default=None, sa_column=Column(JSON))
    tags: Optional[List[str]] = Field(default_factory=list, sa_column=Column(JSON))
    user_id: str

    def model_post_init(self, __context):
        # Validate that reminder_time is not after due_date
        if self.due_date and self.reminder_time and self.reminder_time > self.due_date:
            raise ValueError("Reminder time must be before or equal to due date")


class Task(TaskBase, table=True):
    __tablename__ = "tasks"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    completed: bool = Field(default=False)
    completed_at: Optional[datetime] = None
    # Link to the recurrence series
    series_id: Optional[uuid.UUID] = Field(default=None)
    # For linking to parent task if this is an occurrence
    parent_task_id: Optional[uuid.UUID] = Field(default=None)


class TaskCreateRequest(SQLModel):
    """Request model for creating a task - user_id comes from auth, not from request"""
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = None
    priority: str = "medium"
    due_date: Optional[datetime] = None
    reminder_time: Optional[datetime] = None
    recurrence_pattern: Optional[dict] = Field(default=None, sa_column=Column(JSON))
    tags: Optional[List[str]] = Field(default_factory=list, sa_column=Column(JSON))


class TaskCreate(TaskBase):
    pass


class TaskUpdate(SQLModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    due_date: Optional[datetime] = None
    reminder_time: Optional[datetime] = None
    recurrence_pattern: Optional[dict] = Field(default=None, sa_column=Column(JSON))
    tags: Optional[List[str]] = None
    completed: Optional[bool] = None
    completed_at: Optional[datetime] = None
    series_id: Optional[uuid.UUID] = None


class TaskSeries(SQLModel, table=True):
    """Model for recurring task series - represents a template for recurring tasks"""
    __tablename__ = "task_series"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(sa_column=Column(Text))
    user_id: str
    recurrence_pattern: Optional[Dict[str, Any]] = Field(default=None, sa_column=Column(JSON))
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = Field(default=True)