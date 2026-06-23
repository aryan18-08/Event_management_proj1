import math
from typing import Optional
from sqlalchemy.orm import Session
from app.models.venue import Venue
from app.schemas.venue import VenueCreate, VenueUpdate

def create_venue(db: Session, venue_data: VenueCreate) -> Venue:
    """Create a new venue."""
    venue = Venue(**venue_data.model_dump())
    db.add(venue)
    db.commit()
    db.refresh(venue)
    return venue

def get_venue(db: Session, venue_id: int) -> Optional[Venue]:
    """Get a single venue by ID (excluding soft-deleted)."""
    return (
        db.query(Venue)
        .filter(Venue.id == venue_id, Venue.is_deleted == False)
        .first()
    )

def list_venues(
    db: Session,
    page: int = 1,
    size: int = 10,
    city: Optional[str] = None,
    search: Optional[str] = None,
    sort_by: str = "created_at",
    sort_order: str = "desc",
) -> dict:
    """List venues with pagination, filtering, and sorting."""
    query = db.query(Venue).filter(Venue.is_deleted == False)

    if city:
        query = query.filter(Venue.city.ilike(f"%{city}%"))

    if search:
        query = query.filter(Venue.name.ilike(f"%{search}%"))

    sort_column = getattr(Venue, sort_by, Venue.created_at)
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

def update_venue(db: Session, venue_id: int, venue_data: VenueUpdate) -> Optional[Venue]:
    """Update an existing venue."""
    venue = get_venue(db, venue_id)
    if not venue:
        return None

    update_data = venue_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(venue, field, value)

    db.commit()
    db.refresh(venue)
    return venue

def delete_venue(db: Session, venue_id: int) -> Optional[Venue]:
    """Soft-delete a venue by setting is_deleted = True."""
    venue = get_venue(db, venue_id)
    if not venue:
        return None

    venue.is_deleted = True
    db.commit()
    db.refresh(venue)
    return venue
