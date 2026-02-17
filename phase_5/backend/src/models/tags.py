from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
import uuid
from sqlalchemy import Column, Text

# Association table for many-to-many relationship between tasks and tags
class TaskTagLink(SQLModel, table=True):
    task_id: uuid.UUID = Field(foreign_key="tasks.id", primary_key=True)
    tag_id: uuid.UUID = Field(foreign_key="tags.id", primary_key=True)


class TagBase(SQLModel):
    name: str = Field(min_length=1, max_length=50)
    description: Optional[str] = Field(sa_column=Column(Text))
    user_id: str  # Tags are user-specific


class Tag(TagBase, table=True):
    __tablename__ = "tags"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship with tasks through the association table
    tasks: List["Task"] = Relationship(back_populates="tags", link_model=TaskTagLink)


# Import at the end to avoid circular import
from .task import Task