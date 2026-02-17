from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid
from sqlalchemy import Column, Text, DateTime

class TaskSeriesBase(SQLModel):
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(sa_column=Column(Text))
    recurrence_pattern: dict = Field(sa_column=Column(SQLModel))
    created_by_user_id: str

class TaskSeries(TaskSeriesBase, table=True):
    __tablename__ = "task_series"

    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, sa_column=Column(DateTime))
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column=Column(DateTime))

class TaskSeriesCreate(TaskSeriesBase):
    pass

class TaskSeriesUpdate(SQLModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = None
    recurrence_pattern: Optional[dict] = None