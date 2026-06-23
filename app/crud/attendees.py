import math
from typing import Optional
from sqlalchemy.orm import Session
from app.models.attendee import Attendee
from app.schemas.attendee import AttendeeCreate, AttendeeUpdate

def create_attendee(db: Session, attendee_data: AttendeeCreate) -> Attendee:
    """Create a new attendee."""
    attendee = Attendee(**attendee_data.model_dump())
    db.add(attendee)
    db.commit()
    db.refresh(attendee)
    return attendee

def get_attendee(db: Session, attendee_id: int) -> Optional[Attendee]:
    """Get a single attendee by ID (excluding soft-deleted)."""
    return (
        db.query(Attendee)
        .filter(Attendee.id == attendee_id, Attendee.is_deleted == False)
        .first()
    )

def get_attendee_by_email(db: Session, email: str) -> Optional[Attendee]:
    """Get an attendee by email address (excluding soft-deleted)."""
    return (
        db.query(Attendee)
        .filter(Attendee.email == email, Attendee.is_deleted == False)
        .first()
    )

def list_attendees(
    db: Session,
    page: int = 1,
    size: int = 10,
    search: Optional[str] = None,
    sort_by: str = "created_at",
    sort_order: str = "desc",
) -> dict:
    """List attendees with pagination, search, and sorting."""
    query = db.query(Attendee).filter(Attendee.is_deleted == False)

    if search:
        search_filter = f"%{search}%"
        query = query.filter(
            (Attendee.first_name.ilike(search_filter))
            | (Attendee.last_name.ilike(search_filter))
            | (Attendee.email.ilike(search_filter))
        )

    sort_column = getattr(Attendee, sort_by, Attendee.created_at)
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


def update_attendee(
    db: Session, attendee_id: int, attendee_data: AttendeeUpdate
) -> Optional[Attendee]:
    """Update an existing attendee."""
    attendee = get_attendee(db, attendee_id)
    if not attendee:
        return None

    update_data = attendee_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(attendee, field, value)

    db.commit()
    db.refresh(attendee)
    return attendee


def delete_attendee(db: Session, attendee_id: int) -> Optional[Attendee]:
    """Soft-delete an attendee by setting is_deleted = True."""
    attendee = get_attendee(db, attendee_id)
    if not attendee:
        return None

    attendee.is_deleted = True
    db.commit()
    db.refresh(attendee)
    return attendee
