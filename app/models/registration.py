from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class Registration(Base):
    """Registration model linking an attendee to an event."""

    __tablename__ = "registrations"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False, index=True)
    attendee_id = Column(Integer, ForeignKey("attendees.id"), nullable=False, index=True)
    status = Column(String(20), nullable=False, default="confirmed")
    is_deleted = Column(Boolean, default=False, nullable=False, index=True)
    registered_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    cancelled_at = Column(DateTime(timezone=True), nullable=True)

    # Unique constraint: one active registration per attendee per event
    __table_args__ = (
        UniqueConstraint("event_id", "attendee_id", name="uq_event_attendee"),
    )

    # Relationships
    event = relationship("Event", back_populates="registrations", lazy="joined")
    attendee = relationship("Attendee", back_populates="registrations", lazy="joined")

    def __repr__(self):
        return (
            f"<Registration(id={self.id}, event_id={self.event_id}, "
            f"attendee_id={self.attendee_id}, status='{self.status}')>"
        )
