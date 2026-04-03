# AGENTS.md - Event Management Board

Guide for AI coding agents working in this repository.

## Project Overview

Full-stack event management application:
- **Backend**: Python/Flask API with PostgreSQL, SQLAlchemy, JWT auth
- **Frontend**: React SPA (Create React App) with React Router, Axios
- **Integration**: Ministry Platform API for event syncing

## Build/Lint/Test Commands

### Backend (from `backend/` directory)

```bash
pip install -r requirements.txt   # Install dependencies
python app.py                      # Run dev server (port 5000)
```

No backend test suite or linter is configured.

### Frontend (from `frontend/` directory)

```bash
npm install                        # Install dependencies
npm start                          # Run dev server (port 3000)
npm run build                      # Production build
npm test                           # Run all tests
npm test -- --testPathPattern=EventCard    # Run single test file
npm test -- --coverage             # Run tests with coverage
```

Linting uses CRA's default ESLint (`react-app`, `react-app/jest`). No separate lint command.

## Project Structure

```
event-management-board/
├── backend/
│   ├── app.py              # Flask app factory, blueprint registration
│   ├── models.py           # SQLAlchemy models (User, Event, EventAssignment, EventNote)
│   ├── config.py           # Config classes, TRACKED_ROOMS dict
│   ├── routes/
│   │   ├── auth.py         # /api/auth - register, login, /me
│   │   ├── events.py       # /api/events - CRUD, notes, assignments
│   │   ├── users.py        # /api/users
│   │   └── sync.py         # /api/sync - Ministry Platform sync
│   ├── .env.example        # FLASK_ENV, SECRET_KEY, JWT_SECRET_KEY, DATABASE_URL, MP_*
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/     # EventBoard, EventCard, EventModal, Login
│   │   ├── services/       # api.js (Axios client), AuthContext.js
│   │   ├── styles/         # One CSS file per component
│   │   ├── App.js          # Router with PrivateRoute guard
│   │   └── index.js
│   └── package.json        # proxy: http://localhost:5000
└── AGENTS.md
```

## Backend Code Style

### Imports

Grouped by: third-party packages, then local modules. Standard library mixed in with third-party.

```python
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Event, EventNote, EventAssignment, User
from datetime import datetime
```

### Naming Conventions

- **Variables/functions/modules**: snake_case
- **Classes**: PascalCase (`EventAssignment`)
- **Blueprints**: `{name}_bp` (`events_bp`, `auth_bp`, `sync_bp`, `users_bp`)
- **Route functions**: descriptive verbs (`get_events`, `add_note`, `sync_events`)

### Models

- Each model has a `to_dict()` method for JSON serialization
- Docstrings on classes and methods
- Relationships use `backref` for reverse access
- Timestamps: `created_at`, `updated_at` with `default=datetime.utcnow`

### Routes

- Flask blueprints organized by domain, registered at `/api/{domain}`
- Protected endpoints use `@jwt_required()` decorator
- Returns tuples: `(jsonify({...}), status_code)`
- Error format: `{'error': 'message'}` — Success format: `{'message': '...'}` or model dict
- HTTP status: 400 (validation), 401 (auth failed), 403 (unauthorized), 404 (not found), 409 (conflict), 201 (created)

### Error Handling

- Validate input: `if not data or 'field' not in data` → return 400
- Ownership checks: compare `note.user_id != user_id` → return 403
- External API calls wrapped in try/except with specific exception types (see `sync.py`)
- Use `current_app.config[...]` to access config in routes

### Configuration

- Base `Config` class with `DevelopmentConfig`/`ProductionConfig` subclasses
- Secrets from environment variables with hardcoded dev fallbacks
- `TRACKED_ROOMS` dict maps room IDs to names in `config.py`

## Frontend Code Style

### Imports (order)

1. React and React packages (`react`, `react-router-dom`)
2. Third-party libraries (`date-fns`)
3. Local services (`../services/api`, `../services/AuthContext`)
4. Local components (`./EventCard`)
5. CSS (`../styles/EventBoard.css`)

### Component Structure

- Functional components with hooks only (no class components)
- PascalCase filenames (`EventCard.js`)
- Default exports for all components
- Props destructured in function signature: `({ event, onClick }) =>`

### State and Hooks

- `useState` for local state
- `useEffect` for data fetching on mount
- `useAuth()` from `AuthContext` for authentication state
- `useParams()` for route params, `useNavigate()` for navigation

### API Calls

- Centralized in `services/api.js` using Axios
- Organized by domain: `authAPI`, `eventsAPI`, `syncAPI`, `usersAPI`
- Axios interceptor adds JWT from `localStorage` to all requests
- Async/await with try/catch in components:

```javascript
const fetchData = async () => {
  try {
    const response = await eventsAPI.getEvents();
    setData(response.data);
  } catch (error) {
    console.error('Failed:', error);
  }
};
```

### Naming Conventions

- **Variables/functions/props**: camelCase
- **Components**: PascalCase
- **CSS classes**: kebab-case in both CSS and JSX `className`
- **Event handlers**: `handle{Action}` (`handleSync`, `handleEventClick`)
- **Setter naming**: `const [loading, setLoading] = useState(false)`

### Styling

- One CSS file per major component in `src/styles/`
- CSS files imported at top of component file
- Conditional classes: `` className={`event-card ${event.cancelled ? 'cancelled' : ''}} ``

### Error Handling

- Guard rendering with `{event && <Component />}`
- Loading states: `if (loading) return <div>Loading...</div>`
- `console.error` for logging, `alert()` for user-facing errors (current pattern)
- `error.response?.data?.error` to extract backend error messages

## Key Conventions

- **Never commit `.env` files** — they contain secrets
- JWT identity is `str(user.id)`, converted back with `int(get_jwt_identity())`
- Frontend proxies API calls to `http://localhost:5000` via CRA proxy setting
- Ministry Platform sync requires valid `MP_BEARER_TOKEN` env var
- Tracked rooms are configured in `backend/config.py` `TRACKED_ROOMS` dict
