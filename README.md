# Event Management API

A comprehensive RESTful API for managing events, venues, attendees, and registrations built with **FastAPI**, **PostgreSQL**, **SQLAlchemy**, and **Alembic**.

## Features

- **CRUD operations** for Events, Venues, Attendees, and Registrations
- **Venue capacity enforcement** — prevents over-booking automatically
- **Soft delete** across all entities
- **Pagination** on all list endpoints
- **Filtering & Sorting** — search events by title, date, venue, or status
- **Request validation** via Pydantic models
- **Proper HTTP status codes** and structured error responses
- **Swagger UI** auto-generated API documentation

## Tech Stack

| Technology   | Purpose                |
|-------------|------------------------|
| FastAPI      | Web framework          |
| PostgreSQL   | Database               |
| SQLAlchemy   | ORM                    |
| Alembic      | Database migrations    |
| Pydantic     | Request/response validation |

## Project Structure

```
Event_management_proj1/
├── alembic/                    # Database migrations
│   ├── versions/
│   └── env.py
├── app/
│   ├── main.py                 # FastAPI entry point
│   ├── config.py               # Settings (from .env)
│   ├── database.py             # SQLAlchemy setup
│   ├── models/                 # ORM models
│   ├── schemas/                # Pydantic schemas
│   ├── routers/                # API endpoints
│   └── crud/                   # Database operations
├── .env                        # Environment variables
├── alembic.ini                 # Alembic config
├── requirements.txt            # Python dependencies
└── README.md
```

## Setup & Installation

### 1. Create and activate virtual environment

```bash
python -m venv venv

# Windows
.\venv\Scripts\activate

```
### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure the database

Create a `.env` file in the project root:

```
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/events
```

### 4. Create the PostgreSQL database

```bash
psql -U postgres
CREATE DATABASE events;
\q
```

### 5. Run database migrations

```bash
alembic upgrade head
```

### 6. Start the server

```bash
uvicorn app.main:app --reload
```

The API will be available at: **http://localhost:8000**

## API Documentation

Once the server is running:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Venues (`/api/v1/venues`)

| Method | Endpoint         | Description              |
|--------|-----------------|--------------------------|
| POST   | `/`             | Create a new venue       |
| GET    | `/`             | List venues (paginated)  |
| GET    | `/{id}`         | Get venue by ID          |
| PUT    | `/{id}`         | Update venue             |
| DELETE | `/{id}`         | Soft-delete venue        |

### Events (`/api/v1/events`)

| Method | Endpoint         | Description                        |
|--------|------------------|------------------------------------|
| POST   | `/`              | Create a new event                 |
| GET    | `/`              | List events (paginated + filters)  |
| GET    | `/upcoming`      | List upcoming events               |
| GET    | `/past`          | List past events                   |
| GET    | `/{id}`          | Get event by ID                    |
| PUT    | `/{id}`          | Update event                       |
| DELETE | `/{id}`          | Soft-delete event                  |

**Query Parameters for `GET /`**: `title`, `venue_id`, `status`, `start_date`, `end_date`, `sort_by`, `sort_order`, `page`, `size`

### Attendees (`/api/v1/attendees`)

| Method | Endpoint         | Description                 |
|--------|------------------|-----------------------------|
| POST   | `/`              | Create a new attendee       |
| GET    | `/`              | List attendees (paginated)  |
| GET    | `/{id}`          | Get attendee by ID          |
| PUT    | `/{id}`          | Update attendee             |
| DELETE | `/{id}`          | Soft-delete attendee        |

### Registrations (`/api/v1/registrations`)

| Method | Endpoint              | Description                  |
|--------|----------------------|------------------------------|
| POST   | `/`                  | Register attendee for event  |
| GET    | `/`                  | List registrations           |
| GET    | `/{id}`              | Get registration by ID       |
| PATCH  | `/{id}/cancel`       | Cancel a registration        |
| DELETE | `/{id}`              | Soft-delete registration     |

## Business Rules

1. **Capacity Enforcement**: Registrations are blocked when the event's venue has reached its capacity limit (HTTP 409).
2. **Unique Registrations**: An attendee can only have one active registration per event.
3. **Cancellation**: Cancelling a registration sets its status to `"cancelled"` and frees up capacity.
4. **Soft Delete**: All entities use an `is_deleted` flag instead of being physically removed from the database.
5. **Event Status**: Events can be `scheduled`, `ongoing`, `completed`, or `cancelled`.
