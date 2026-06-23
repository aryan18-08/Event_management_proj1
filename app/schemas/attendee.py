from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr

class AttendeeCreate(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=100, description="First name")
    last_name: str = Field(..., min_length=1, max_length=100, description="Last name")
    email: str = Field(
        ..., min_length=1, max_length=255, description="Email address",
        pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",
    )
    phone: Optional[str] = Field(None, max_length=20, description="Phone number")

class AttendeeUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[str] = Field(
        None, max_length=255,
        pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",
    )
    phone: Optional[str] = Field(None, max_length=20)

class AttendeeResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    phone: Optional[str]
    is_deleted: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class AttendeeListResponse(BaseModel):
    items: List[AttendeeResponse]
    total: int
    page: int
    size: int
    pages: int
