from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.event import EventCreate, EventUpdate, EventResponse, EventListResponse
from app.crud import events as event_crud
from app.crud import venues as venue_crud

router = APIRouter(prefix="/api/v1/events", tags=["Events"])

@router.post("/", response_model=EventResponse, status_code=status.HTTP_201_CREATED)
def create_event(event_data: EventCreate, db: Session = Depends(get_db)):
    """Create a new event. The venue must exist."""
    venue = venue_crud.get_venue(db, event_data.venue_id)
    if not venue:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Venue with id {event_data.venue_id} not found",
        )
    return event_crud.create_event(db, event_data)

@router.get("/", response_model=EventListResponse)
def list_events(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(10, ge=1, le=100, description="Items per page"),
    title: Optional[str] = Query(None, description="Search by event title"),
    venue_id: Optional[int] = Query(None, description="Filter by venue ID"),
    event_status: Optional[str] = Query(
        None, alias="status", description="Filter by status (scheduled, ongoing, completed, cancelled)"
    ),
    start_date: Optional[datetime] = Query(None, description="Filter events starting after this date"),
    end_date: Optional[datetime] = Query(None, description="Filter events ending before this date"),
    sort_by: str = Query("start_date", description="Sort field (title, start_date, created_at)"),
    sort_order: str = Query("desc", description="Sort order (asc or desc)"),
    db: Session = Depends(get_db),
):
    """List all events with pagination, filtering, and sorting."""
    return event_crud.list_events(
        db, page, size, title, venue_id, event_status, start_date, end_date, sort_by, sort_order
    )

@router.get("/upcoming", response_model=EventListResponse)
def list_upcoming_events(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(10, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db),
):
    """List upcoming events (start_date in the future)."""
    return event_crud.list_upcoming_events(db, page, size)

@router.get("/past", response_model=EventListResponse)
def list_past_events(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(10, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db),
):
    """List past events (end_date in the past)."""
    return event_crud.list_past_events(db, page, size)

@router.get("/{event_id}", response_model=EventResponse)
def get_event(event_id: int, db: Session = Depends(get_db)):
    """Get an event by ID."""
    event = event_crud.get_event(db, event_id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Event with id {event_id} not found",
        )
    return event

@router.put("/{event_id}", response_model=EventResponse)
def update_event(event_id: int, event_data: EventUpdate, db: Session = Depends(get_db)):
    """Update an existing event."""
    # If venue_id is being updated, validate it exists
    if event_data.venue_id is not None:
        venue = venue_crud.get_venue(db, event_data.venue_id)
        if not venue:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Venue with id {event_data.venue_id} not found",
            )

    event = event_crud.update_event(db, event_id, event_data)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Event with id {event_id} not found",
        )
    return event

@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_event(event_id: int, db: Session = Depends(get_db)):
    """Soft-delete an event."""
    event = event_crud.delete_event(db, event_id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Event with id {event_id} not found",
        )
    return None
