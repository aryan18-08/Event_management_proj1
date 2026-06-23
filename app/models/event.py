from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class Event(Base):
    """Event model representing a scheduled event at a venue."""

    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(300), nullable=False, index=True)
    description = Column(Text, nullable=True)
    start_date = Column(DateTime(timezone=True), nullable=False, index=True)
    end_date = Column(DateTime(timezone=True), nullable=False)
    venue_id = Column(Integer, ForeignKey("venues.id"), nullable=False, index=True)
    status = Column(String(20), nullable=False, default="scheduled", index=True)
    is_deleted = Column(Boolean, default=False, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    # Relationships
    venue = relationship("Venue", back_populates="events", lazy="joined")
    registrations = relationship("Registration", back_populates="event", lazy="select")

    def __repr__(self):
        return f"<Event(id={self.id}, title='{self.title}', status='{self.status}')>"
