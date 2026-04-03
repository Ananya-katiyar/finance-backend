from pydantic import BaseModel, EmailStr, field_validator, Field
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)


class RecordCreate(BaseModel):
    amount: float = Field(gt=0, description="Must be greater than 0")
    type: str = Field(description="Must be 'income' or 'expense'")
    category: str = Field(min_length=1)
    date: datetime
    note: Optional[str] = None

    @field_validator("type")
    @classmethod
    def validate_type(cls, v):
        if v not in ("income", "expense"):
            raise ValueError("type must be 'income' or 'expense'")
        return v


class RecordUpdate(BaseModel):
    amount: Optional[float] = Field(default=None, gt=0)
    type: Optional[str] = None
    category: Optional[str] = None
    date: Optional[datetime] = None
    note: Optional[str] = None

    @field_validator("type")
    @classmethod
    def validate_type(cls, v):
        if v is not None and v not in ("income", "expense"):
            raise ValueError("type must be 'income' or 'expense'")
        return v