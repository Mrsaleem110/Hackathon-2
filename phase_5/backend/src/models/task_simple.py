from sqlmodel import SQLModel, Field
from typing import Optional, List
import uuid

class Task(SQLModel, table=True):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = None
    status: str = Field(default="active")
    priority: str = Field(default="medium")
    user_id: str

class TaskCreate(SQLModel):
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = None
    priority: str = "medium"

class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None