from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


# Role Enum
class UserRole(str, Enum):
    viewer = "viewer"
    analyst = "analyst"
    admin = "admin"


# User Table
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    password: str
    role: UserRole = Field(default=UserRole.viewer)
    status: str = "active"


# Financial Record Table
class Record(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    
    amount: float
    type: str  # income / expense
    category: str
    date: datetime
    note: Optional[str] = None

    user_id: Optional[int] = Field(default=None, foreign_key="user.id")