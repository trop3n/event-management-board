# Event Management Board

A full-stack event management application for tracking and managing events in large event spaces. Built to integrate with Ministry Platform API and provide a kanban-style interface for event organization.

## Features

- **Ministry Platform Integration** - Automatically sync events from Ministry Platform API
- **Room-Based Views** - Filter events by specific event spaces (Sanctuary, Smith, Movie Theater, Small Group Rooms)
- **Kanban-Style Board** - Events organized by Today, Tomorrow, Upcoming, and Past
- **Employee Assignments** - Assign team members to events with optional roles
- **Collaborative Notes** - Add notes to events for team communication
- **Real-Time Sync** - Sync latest events from Ministry Platform with one click
- **Responsive Design** - Works on desktop and mobile devices

## Tracked Event Spaces

- 100 - Sanctuary
- 128 - Smith
- 131, 126, 120, 121, 122, 123, 124 - Small Group Rooms
- 226 - Movie Theater

## Tech Stack

### Backend
- Python/Flask
- PostgreSQL
- SQLAlchemy ORM
- Flask-JWT-Extended (authentication)
- Requests (Ministry Platform API integration)

### Frontend
- React
- React Router (routing)
- Axios (API calls)
- date-fns (date formatting)

## Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+
- PostgreSQL 12+
- Ministry Platform API credentials

### 1. Backend Setup

```bash
cd event-management-board/backend

# Install dependencies
pip install -r requirements.txt

# Create PostgreSQL database
sudo -u postgres psql
CREATE DATABASE event_management;
CREATE USER eventuser WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE event_management TO eventuser;
\q

# Configure environment
cp .env.example .env
# Edit .env with your database credentials and Ministry Platform API token

# Run the backend
python app.py
```

Backend will run on http://localhost:5000

### 2. Frontend Setup

```bash
cd event-management-board/frontend

# Install dependencies
npm install

# Configure environment (optional)
cp .env.example .env

# Run the development server
npm start
```

Frontend will open at http://localhost:3000

## Usage

1. **Register/Login** - Create your account or sign in
2. **Sync Events** - Click "Sync Events" to fetch latest events from Ministry Platform
3. **Filter by Room** - Use the room selector dropdown to filter events by specific spaces
4. **View Events** - Events are automatically organized into Today, Tomorrow, Upcoming, and Past columns
5. **Click on Event** - Click any event card to view details
6. **Assign Employees** - In the event modal, select an employee and optional role to assign them
7. **Add Notes** - Add collaborative notes to events for team communication
8. **Manage** - Update or remove assignments and notes as needed

## Project Structure

```
event-management-board/
├── backend/
│   ├── app.py              # Flask application
│   ├── models.py           # Database models (User, Event, EventNote, EventAssignment)
│   ├── config.py           # Configuration (tracked rooms, API settings)
│   ├── routes/
│   │   ├── auth.py         # Authentication routes
│   │   ├── events.py       # Event CRUD and notes/assignments
│   │   ├── users.py        # User routes
│   │   └── sync.py         # Ministry Platform sync
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── EventBoard.js   # Main kanban board
│   │   │   ├── EventCard.js    # Event card component
│   │   │   ├── EventModal.js   # Event details modal
│   │   │   └── Login.js        # Login/register
│   │   ├── services/
│   │   │   ├── api.js          # API client
│   │   │   └── AuthContext.js  # Authentication context
│   │   ├── styles/             # CSS files
│   │   ├── App.js
│   │   └── index.js
│   ├── package.json
│   └── .env.example
│
└── README.md
```

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login and get JWT token
- `GET /api/auth/me` - Get current user

### Events
- `GET /api/events` - Get all events (optional: ?room_id=100)
- `GET /api/events/<id>` - Get specific event
- `POST /api/events/<id>/notes` - Add note to event
- `PUT /api/events/<id>/notes/<note_id>` - Update note
- `DELETE /api/events/<id>/notes/<note_id>` - Delete note
- `POST /api/events/<id>/assignments` - Assign user to event
- `PUT /api/events/<id>/assignments/<assignment_id>` - Update assignment
- `DELETE /api/events/<id>/assignments/<assignment_id>` - Remove assignment

### Sync
- `POST /api/sync/events` - Sync events from Ministry Platform (next 30 days)
- `GET /api/sync/rooms` - Get tracked rooms configuration

### Users
- `GET /api/users` - Get all users
- `GET /api/users/<id>` - Get specific user

## Configuration

### Backend Configuration (config.py)

The `TRACKED_ROOMS` dictionary in config.py defines which room IDs are monitored:

```python
TRACKED_ROOMS = {
    100: 'Sanctuary',
    128: 'Smith',
    # ... add more rooms as needed
}
```

### Ministry Platform API

The application syncs events from Ministry Platform using the stored procedure `api_church_specific_get_events`. Ensure you have:
- Valid API endpoint URL
- Bearer token with appropriate permissions

## Future Enhancements

- Email notifications for event assignments
- Calendar export (iCal)
- Event templates
- Recurring event support
- Advanced filtering (by date range, event type)
- Analytics and reporting
- Mobile app

## License

Internal use only

## Support

For issues or questions, contact the Tech/Production team.
