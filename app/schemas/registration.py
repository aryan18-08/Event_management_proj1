from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

class RegistrationCreate(BaseModel):
    event_id: int = Field(..., gt=0, description="ID of the event")
    attendee_id: int = Field(..., gt=0, description="ID of the attendee")

class AttendeeInRegistration(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    class Config:
        from_attributes = True

class EventInRegistration(BaseModel):
    id: int
    title: str
    start_date: datetime
    end_date: datetime
    status: str
    class Config:
        from_attributes = True

class RegistrationResponse(BaseModel):
    id: int
    event_id: int
    attendee_id: int
    status: str
    is_deleted: bool
    registered_at: datetime
    cancelled_at: Optional[datetime]
    event: Optional[EventInRegistration] = None
    attendee: Optional[AttendeeInRegistration] = None
    class Config:
        from_attributes = True

class RegistrationListResponse(BaseModel):
    items: List[RegistrationResponse]
    total: int
    page: int
    size: int
    pages: int
