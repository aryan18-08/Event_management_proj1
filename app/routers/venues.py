from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.venue import VenueCreate, VenueUpdate, VenueResponse, VenueListResponse
from app.crud import venues as venue_crud

router = APIRouter(prefix="/api/v1/venues", tags=["Venues"])

@router.post("/", response_model=VenueResponse, status_code=status.HTTP_201_CREATED)
def create_venue(venue_data: VenueCreate, db: Session = Depends(get_db)):
    """Create a new venue."""
    return venue_crud.create_venue(db, venue_data)

@router.get("/", response_model=VenueListResponse)
def list_venues(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(10, ge=1, le=100, description="Items per page"),
    city: Optional[str] = Query(None, description="Filter by city"),
    search: Optional[str] = Query(None, description="Search by venue name"),
    sort_by: str = Query("created_at", description="Sort field (name, city, capacity, created_at)"),
    sort_order: str = Query("desc", description="Sort order (asc or desc)"),
    db: Session = Depends(get_db),
):
    return venue_crud.list_venues(db, page, size, city, search, sort_by, sort_order)

@router.get("/{venue_id}", response_model=VenueResponse)
def get_venue(venue_id: int, db: Session = Depends(get_db)):
    venue = venue_crud.get_venue(db, venue_id)
    if not venue:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Venue with id {venue_id} not found",
        )
    return venue

@router.put("/{venue_id}", response_model=VenueResponse)
def update_venue(venue_id: int, venue_data: VenueUpdate, db: Session = Depends(get_db)):
    venue = venue_crud.update_venue(db, venue_id, venue_data)
    if not venue:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Venue with id {venue_id} not found",
        )
    return venue

@router.delete("/{venue_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_venue(venue_id: int, db: Session = Depends(get_db)):
    venue = venue_crud.delete_venue(db, venue_id)
    if not venue:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Venue with id {venue_id} not found",
        )
    return None
