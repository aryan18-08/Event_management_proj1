import math
from datetime import datetime, timezone
from typing import Optional
from sqlalchemy.orm import Session
from app.models.event import Event
from app.schemas.event import EventCreate, EventUpdate

def create_event(db: Session, event_data: EventCreate) -> Event:
    """Create a new event."""
    event = Event(**event_data.model_dump())
    db.add(event)
    db.commit()
    db.refresh(event)
    return event

def get_event(db: Session, event_id: int) -> Optional[Event]:
    """Get a single event by ID (excluding soft-deleted)."""
    return (
        db.query(Event)
        .filter(Event.id == event_id, Event.is_deleted == False)
        .first()
    )

def list_events(
    db: Session,
    page: int = 1,
    size: int = 10,
    title: Optional[str] = None,
    venue_id: Optional[int] = None,
    status: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    sort_by: str = "start_date",
    sort_order: str = "desc",
) -> dict:
    """List events with pagination, filtering, and sorting."""
    query = db.query(Event).filter(Event.is_deleted == False)

    if title:
        query = query.filter(Event.title.ilike(f"%{title}%"))

    if venue_id:
        query = query.filter(Event.venue_id == venue_id)

    if status:
        query = query.filter(Event.status == status)

    if start_date:
        query = query.filter(Event.start_date >= start_date)

    if end_date:
        query = query.filter(Event.end_date <= end_date)

    # Sorting
    sort_column = getattr(Event, sort_by, Event.start_date)
    if sort_order.lower() == "asc":
        query = query.order_by(sort_column.asc())
    else:
        query = query.order_by(sort_column.desc())

    # Pagination
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


def list_upcoming_events(db: Session, page: int = 1, size: int = 10) -> dict:
    """List events that haven't started yet."""
    now = datetime.now(timezone.utc)
    query = (
        db.query(Event)
        .filter(Event.is_deleted == False, Event.start_date > now)
        .order_by(Event.start_date.asc())
    )

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

def list_past_events(db: Session, page: int = 1, size: int = 10) -> dict:
    """List events that have already ended."""
    now = datetime.now(timezone.utc)
    query = (
        db.query(Event)
        .filter(Event.is_deleted == False, Event.end_date < now)
        .order_by(Event.end_date.desc())
    )
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

def update_event(db: Session, event_id: int, event_data: EventUpdate) -> Optional[Event]:
    """Update an existing event."""
    event = get_event(db, event_id)
    if not event:
        return None

    update_data = event_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(event, field, value)

    db.commit()
    db.refresh(event)
    return event

def delete_event(db: Session, event_id: int) -> Optional[Event]:
    """Soft-delete an event by setting is_deleted = True."""
    event = get_event(db, event_id)
    if not event:
        return None

    event.is_deleted = True
    db.commit()
    db.refresh(event)
    return event
