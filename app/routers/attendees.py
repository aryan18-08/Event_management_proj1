from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.attendee import (
    AttendeeCreate,
    AttendeeUpdate,
    AttendeeResponse,
    AttendeeListResponse,
)
from app.crud import attendees as attendee_crud

router = APIRouter(prefix="/api/v1/attendees", tags=["Attendees"])

@router.post("/", response_model=AttendeeResponse, status_code=status.HTTP_201_CREATED)
def create_attendee(attendee_data: AttendeeCreate, db: Session = Depends(get_db)):
    """Create a new attendee. Email must be unique."""
    existing = attendee_crud.get_attendee_by_email(db, attendee_data.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"An attendee with email '{attendee_data.email}' already exists",
        )
    try:
        return attendee_crud.create_attendee(db, attendee_data)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"An attendee with email '{attendee_data.email}' already exists",
        )

@router.get("/", response_model=AttendeeListResponse)
def list_attendees(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(10, ge=1, le=100, description="Items per page"),
    search: Optional[str] = Query(None, description="Search by name or email"),
    sort_by: str = Query("created_at", description="Sort field (first_name, last_name, email, created_at)"),
    sort_order: str = Query("desc", description="Sort order (asc or desc)"),
    db: Session = Depends(get_db),
):
    """List all attendees with pagination, search, and sorting."""
    return attendee_crud.list_attendees(db, page, size, search, sort_by, sort_order)

@router.get("/{attendee_id}", response_model=AttendeeResponse)
def get_attendee(attendee_id: int, db: Session = Depends(get_db)):
    """Get an attendee by ID."""
    attendee = attendee_crud.get_attendee(db, attendee_id)
    if not attendee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Attendee with id {attendee_id} not found",
        )
    return attendee

@router.put("/{attendee_id}", response_model=AttendeeResponse)
def update_attendee(
    attendee_id: int, attendee_data: AttendeeUpdate, db: Session = Depends(get_db)
):
    """Update an existing attendee."""
    if attendee_data.email:
        existing = attendee_crud.get_attendee_by_email(db, attendee_data.email)
        if existing and existing.id != attendee_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"An attendee with email '{attendee_data.email}' already exists",
            )
        
    attendee = attendee_crud.update_attendee(db, attendee_id, attendee_data)
    if not attendee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Attendee with id {attendee_id} not found",
        )
    return attendee

@router.delete("/{attendee_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_attendee(attendee_id: int, db: Session = Depends(get_db)):
    """Soft-delete an attendee."""
    attendee = attendee_crud.delete_attendee(db, attendee_id)
    if not attendee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Attendee with id {attendee_id} not found",
        )
    return None
