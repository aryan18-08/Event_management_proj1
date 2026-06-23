from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

class VenueCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200, description="Venue name")
    address: str = Field(..., min_length=1, max_length=500, description="Full address")
    city: str = Field(..., min_length=1, max_length=100, description="City name")
    capacity: int = Field(..., gt=0, description="Maximum number of attendees")
    description: Optional[str] = Field(None, description="Optional venue description")

class VenueUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    address: Optional[str] = Field(None, min_length=1, max_length=500)
    city: Optional[str] = Field(None, min_length=1, max_length=100)
    capacity: Optional[int] = Field(None, gt=0)
    description: Optional[str] = None

class VenueResponse(BaseModel):
    id: int
    name: str
    address: str
    city: str
    capacity: int
    description: Optional[str]
    is_deleted: bool
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True

class VenueListResponse(BaseModel):
    items: List[VenueResponse]
    total: int
    page: int
    size: int
    pages: int
