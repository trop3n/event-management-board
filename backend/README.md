# Event Management Board - Backend

Flask-based backend API for managing events from Ministry Platform.

## Features

- Ministry Platform API integration
- Event syncing for tracked rooms
- Employee assignment to events
- Event notes and collaboration
- JWT authentication

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment:
```bash
cp .env.example .env
# Edit .env with your credentials
```

3. Create PostgreSQL database:
```bash
sudo -u postgres psql
CREATE DATABASE event_management;
CREATE USER eventuser WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE event_management TO eventuser;
\q
```

4. Run the application:
```bash
python app.py
```

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login
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
- `POST /api/sync/events` - Sync events from Ministry Platform
- `GET /api/sync/rooms` - Get tracked rooms

### Users
- `GET /api/users` - Get all users
- `GET /api/users/<id>` - Get specific user
