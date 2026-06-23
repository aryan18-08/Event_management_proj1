import math
from datetime import datetime, timezone
from typing import Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.registration import Registration
from app.models.event import Event
from app.models.attendee import Attendee
from app.schemas.registration import RegistrationCreate

def create_registration(db: Session, registration_data: RegistrationCreate) -> Registration:
    event = (
        db.query(Event)
        .filter(Event.id == registration_data.event_id, Event.is_deleted == False)
        .first()
    )
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Event with id {registration_data.event_id} not found",
        )
    
    attendee = (
        db.query(Attendee)
        .filter(Attendee.id == registration_data.attendee_id, Attendee.is_deleted == False)
        .first()
    )
    if not attendee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Attendee with id {registration_data.attendee_id} not found",
        )

    if event.status in ("cancelled", "completed"):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Cannot register for an event with status '{event.status}'",
        )

    existing = (
        db.query(Registration)
        .filter(
            Registration.event_id == registration_data.event_id,
            Registration.attendee_id == registration_data.attendee_id,
            Registration.status == "confirmed",
            Registration.is_deleted == False,
        ).first()
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Attendee is already registered for this event",
        )
    
    active_count = (
        db.query(Registration)
        .filter(
            Registration.event_id == registration_data.event_id,
            Registration.status == "confirmed",
            Registration.is_deleted == False,
        ).count()
    )
    if active_count >= event.venue.capacity:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Event has reached maximum capacity ({event.venue.capacity})",
        )

    registration = Registration(
        event_id=registration_data.event_id,
        attendee_id=registration_data.attendee_id,
        status="confirmed",
    )
    db.add(registration)
    db.commit()
    db.refresh(registration)
    return registration


def get_registration(db: Session, registration_id: int) -> Optional[Registration]:
    """Get a single registration by ID (excluding soft-deleted)."""
    return (
        db.query(Registration)
        .filter(Registration.id == registration_id, Registration.is_deleted == False)
        .first()
    )

def list_registrations(
    db: Session,
    page: int = 1,
    size: int = 10,
    event_id: Optional[int] = None,
    attendee_id: Optional[int] = None,
    registration_status: Optional[str] = None,
    sort_by: str = "registered_at",
    sort_order: str = "desc",
) -> dict:
    """List registrations with pagination, filtering, and sorting."""
    query = db.query(Registration).filter(Registration.is_deleted == False)

    if event_id:
        query = query.filter(Registration.event_id == event_id)

    if attendee_id:
        query = query.filter(Registration.attendee_id == attendee_id)

    if registration_status:
        query = query.filter(Registration.status == registration_status)

    sort_column = getattr(Registration, sort_by, Registration.registered_at)
    if sort_order.lower() == "asc":
        query = query.order_by(sort_column.asc())
    else:
        query = query.order_by(sort_column.desc())

    total = query.count()
    pages = math.ceil(total / size) if size > 0 else 0
    items = query.offset((page - 1) * size).limit(size).all()

    return {
        "items": items,
        "total": total,
        "page": page,
        "size": size,
        "pages": pages,
    }

def cancel_registration(db: Session, registration_id: int) -> Optional[Registration]:
    """Cancel a registration (soft-cancel: set status to cancelled)."""
    registration = get_registration(db, registration_id)
    if not registration:
        return None

    if registration.status == "cancelled":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Registration is already cancelled",
        )

    registration.status = "cancelled"
    registration.cancelled_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(registration)
    return registration

def delete_registration(db: Session, registration_id: int) -> Optional[Registration]:
    """Soft-delete a registration by setting is_deleted = True."""
    registration = get_registration(db, registration_id)
    if not registration:
        return None

    registration.is_deleted = True
    db.commit()
    db.refresh(registration)
    return registration
