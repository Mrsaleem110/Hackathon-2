from sqlmodel import SQLModel, Field, Column, DateTime
from typing import Optional
from datetime import datetime
import uuid


class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)
    name: Optional[str] = Field(default=None)
    is_active: bool = Field(default=True)


class User(UserBase, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    hashed_password: str
    created_at: datetime = Field(sa_column=Column(DateTime, default=datetime.utcnow))
    updated_at: datetime = Field(sa_column=Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow))


class UserCreate(UserBase):
    password: str


class UserUpdate(SQLModel):
    name: Optional[str] = None
    email: Optional[str] = None
    is_active: Optional[bool] = None


class UserPublic(UserBase):
    id: str
    created_at: datetime