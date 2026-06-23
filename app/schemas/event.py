from datetime import datetime
from typing import Optional, List
from enum import Enum
from pydantic import BaseModel, Field, model_validator

class EventStatus(str, Enum):
    SCHEDULED = "scheduled"
    ONGOING = "ongoing"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class EventCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=300, description="Event title")
    description: Optional[str] = Field(None, description="Event description")
    start_date: datetime = Field(..., description="Event start date and time")
    end_date: datetime = Field(..., description="Event end date and time")
    venue_id: int = Field(..., gt=0, description="ID of the venue hosting the event")
    status: EventStatus = Field(
        default=EventStatus.SCHEDULED, description="Event status"
    )
    @model_validator(mode="after")
    def validate_dates(self):
        """Ensure start_date is before end_date."""
        if self.start_date >= self.end_date:
            raise ValueError("start_date must be before end_date")
        return self

class EventUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=300)
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    venue_id: Optional[int] = Field(None, gt=0)
    status: Optional[EventStatus] = None
    @model_validator(mode="after")
    def validate_dates(self):
        """If both dates are provided, ensure start_date is before end_date."""
        if self.start_date and self.end_date and self.start_date >= self.end_date:
            raise ValueError("start_date must be before end_date")
        return self

class VenueInEvent(BaseModel):
    id: int
    name: str
    city: str
    capacity: int
    class Config:
        from_attributes = True

class EventResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    start_date: datetime
    end_date: datetime
    venue_id: int
    status: str
    is_deleted: bool
    created_at: datetime
    updated_at: datetime
    venue: Optional[VenueInEvent] = None
    class Config:
        from_attributes = True

class EventListResponse(BaseModel):
    items: List[EventResponse]
    total: int
    page: int
    size: int
    pages: int
