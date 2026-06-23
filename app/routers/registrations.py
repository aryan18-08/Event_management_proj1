from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.registration import (
    RegistrationCreate,
    RegistrationResponse,
    RegistrationListResponse,
)
from app.crud import registrations as registration_crud

router = APIRouter(prefix="/api/v1/registrations", tags=["Registrations"])

@router.post("/", response_model=RegistrationResponse, status_code=status.HTTP_201_CREATED)
def create_registration(
    registration_data: RegistrationCreate, db: Session = Depends(get_db)
):
    return registration_crud.create_registration(db, registration_data)

@router.get("/", response_model=RegistrationListResponse)
def list_registrations(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(10, ge=1, le=100, description="Items per page"),
    event_id: Optional[int] = Query(None, description="Filter by event ID"),
    attendee_id: Optional[int] = Query(None, description="Filter by attendee ID"),
    registration_status: Optional[str] = Query(
        None, alias="status", description="Filter by status (confirmed, cancelled)"
    ),
    sort_by: str = Query(
        "registered_at", description="Sort field (registered_at, status)"
    ),
    sort_order: str = Query("desc", description="Sort order (asc or desc)"),
    db: Session = Depends(get_db),
):
    """List all registrations with pagination, filtering, and sorting."""
    return registration_crud.list_registrations(
        db, page, size, event_id, attendee_id, registration_status, sort_by, sort_order
    )

@router.get("/{registration_id}", response_model=RegistrationResponse)
def get_registration(registration_id: int, db: Session = Depends(get_db)):
    """Get a registration by ID."""
    registration = registration_crud.get_registration(db, registration_id)
    if not registration:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Registration with id {registration_id} not found",
        )
    return registration

@router.patch("/{registration_id}/cancel", response_model=RegistrationResponse)
def cancel_registration(registration_id: int, db: Session = Depends(get_db)):
    """Cancel a registration. This frees up capacity for the event."""
    registration = registration_crud.cancel_registration(db, registration_id)
    if not registration:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Registration with id {registration_id} not found",
        )
    return registration

@router.delete("/{registration_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_registration(registration_id: int, db: Session = Depends(get_db)):
    """Soft-delete a registration."""
    registration = registration_crud.delete_registration(db, registration_id)
    if not registration:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Registration with id {registration_id} not found",
        )
    return None
