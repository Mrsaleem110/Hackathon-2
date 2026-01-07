from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime
import uuid
from enum import Enum

class TaskBase(SQLModel):
    title: str
    description: Optional[str] = None
    completed: bool = False
    user_id: str

class Task(TaskBase, table=True):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default=datetime.utcnow())
    updated_at: datetime = Field(default=datetime.utcnow())

class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

class TaskCreate(TaskBase):
    pass