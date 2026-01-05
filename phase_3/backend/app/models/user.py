from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .item import Item
    from .session import Session


class UserBase(SQLModel):
    email: str = Field(unique=True, nullable=False)
    username: str = Field(unique=True, nullable=False)
    first_name: str
    last_name: str


class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to items - using string reference to avoid circular import
    items: List["Item"] = Relationship(back_populates="owner")
    # Relationship to sessions - using string reference to avoid circular import
    sessions: List["Session"] = Relationship(back_populates="user")


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int
    is_active: bool
    created_at: datetime


class UserUpdate(SQLModel):
    email: Optional[str] = None
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: Optional[bool] = None


class UserLogin(BaseModel):
    username: str
    password: str