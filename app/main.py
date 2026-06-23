from fastapi import FastAPI
from app.routers import venues, events, attendees, registrations

app = FastAPI(
    title="Event Management API",
    description=(
        "A comprehensive RESTful API for managing events, venues, attendees, "
        "and registrations. Features include venue capacity enforcement, "
        "event filtering/sorting, pagination, and soft-delete support."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_tags=[
        {
            "name": "Venues",
            "description": "Manage event venues with capacity limits.",
        },
        {
            "name": "Events",
            "description": "Create, update, and search events. Filter by title, date, venue, or status.",
        },
        {
            "name": "Attendees",
            "description": "Manage attendees with unique email enforcement.",
        },
        {
            "name": "Registrations",
            "description": "Register attendees for events with automatic capacity enforcement.",
        },
    ],
)

app.include_router(venues.router)
app.include_router(events.router)
app.include_router(attendees.router)
app.include_router(registrations.router)

@app.get("/", tags=["Health"])
def root():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "Event Management API",
        "version": "1.0.0",
    }
