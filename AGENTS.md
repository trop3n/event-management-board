# AGENTS.md - Event Management Board

Guide for AI coding agents working in this repository.

## Project Overview

Full-stack event management application with:
- **Backend**: Python/Flask API with PostgreSQL
- **Frontend**: React SPA with React Router
- **Integration**: Ministry Platform API for event syncing

## Build/Lint/Test Commands

### Backend (from `backend/` directory)

```bash
# Install dependencies
pip install -r requirements.txt

# Run development server
python app.py

# Run production (with gunicorn, not yet in requirements)
gunicorn app:app

# Database setup (PostgreSQL required)
sudo -u postgres psql -c "CREATE DATABASE event_management;"
sudo -u postgres psql -c "CREATE USER eventuser WITH PASSWORD 'your_password';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE event_management TO eventuser;"

# Configure environment
cp .env.example .env
# Edit .env with DATABASE_URL, SECRET_KEY, JWT_SECRET_KEY, MP_BEARER_TOKEN
```

### Frontend (from `frontend/` directory)

```bash
# Install dependencies
npm install

# Run development server (opens at http://localhost:3000)
npm start

# Build for production
npm run build

# Run tests
npm test

# Run a single test file
npm test -- --testPathPattern=EventCard

# Run tests with coverage
npm test -- --coverage
```

### No explicit linting setup
The project uses Create React App's default ESLint configuration (`react-app`, `react-app/jest`).

## Code Style Guidelines

### Python Backend

**Imports (order):**
1. Standard library (alphabetically)
2. Third-party packages (Flask, SQLAlchemy, etc.)
3. Local modules (models, config)

```python
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Event, User
from datetime import datetime
```

**Naming Conventions:**
- Snake_case for variables, functions, modules
- PascalCase for classes (e.g., `EventAssignment`)
- Blueprint naming: `{name}_bp` (e.g., `events_bp`)
- Route functions: descriptive verbs (e.g., `get_events`, `add_note`)

**Models:**
- Each model has a `to_dict()` method for JSON serialization
- Use docstrings for class and method documentation
- Relationships use `backref` for reverse access
- Timestamps: `created_at`, `updated_at` with `datetime.utcnow`

**Routes:**
- Use Flask blueprints organized by domain (`auth`, `events`, `users`, `sync`)
- Decorate with `@jwt_required()` for protected endpoints
- Return tuples: `(jsonify(...), status_code)`
- Error responses: `{'error': 'message'}` with appropriate HTTP status
- Success responses: `{'message': '...'}` or return object data

**Error Handling:**
- Check for missing data: `if not data or 'field' not in data`
- Return 400 for validation errors, 404 for not found, 403 for unauthorized, 409 for conflicts
- Use try/except for external API calls (see `sync.py`)

**Configuration:**
- Config classes inherit from base `Config`
- Environment-based: `DevelopmentConfig`, `ProductionConfig`
- Secrets from environment variables with fallbacks

### React Frontend

**Imports (order):**
1. React and React-related packages
2. Third-party libraries (axios, date-fns)
3. Local components (relative paths)
4. CSS/styles (last)

```javascript
import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { eventsAPI } from '../services/api';
import EventCard from './EventCard';
import '../styles/EventBoard.css';
```

**Component Structure:**
- Functional components with hooks (no class components)
- Component files: PascalCase (e.g., `EventCard.js`)
- Default exports for components
- Props destructuring in function signature

```javascript
const EventCard = ({ event, onClick }) => {
  // hooks and logic
  return ( /* JSX */ );
};
export default EventCard;
```

**Hooks Usage:**
- `useState` for local state
- `useEffect` for side effects (data fetching, subscriptions)
- `useContext` with `AuthProvider` for authentication
- `useParams` for route parameters, `useNavigate` for navigation

**API Calls:**
- Centralized in `services/api.js`
- Organized by domain: `authAPI`, `eventsAPI`, `syncAPI`, `usersAPI`
- Use async/await pattern
- Handle errors with try/catch

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

**Naming Conventions:**
- camelCase for variables, functions, props
- PascalCase for component names
- CSS classes: kebab-case in CSS, camelCase or kebab-case in JSX className
- Handler functions: `handle{Action}` (e.g., `handleClick`, `handleSync`)

**Styling:**
- CSS files in `src/styles/` directory
- One CSS file per major component
- Import CSS at top of component file

**Error Handling:**
- Check for null/undefined before rendering: `{event && <Component />}`
- Provide loading states
- Use try/catch for async operations
- Console.error for logging (no alert in production)

## Project Structure

```
event-management-board/
├── backend/
│   ├── app.py              # Flask app factory
│   ├── models.py           # SQLAlchemy models
│   ├── config.py           # Configuration classes
│   ├── routes/
│   │   ├── auth.py         # Authentication endpoints
│   │   ├── events.py       # Event CRUD, notes, assignments
│   │   ├── users.py        # User endpoints
│   │   └── sync.py         # Ministry Platform sync
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── services/       # API client, AuthContext
│   │   ├── styles/         # CSS files
│   │   ├── App.js          # Main app with routing
│   │   └── index.js        # Entry point
│   └── package.json
└── README.md
```

## Important Notes

- **Never commit `.env` files** - they contain secrets
- **JWT tokens** stored in localStorage on frontend
- **Ministry Platform sync** requires valid `MP_BEARER_TOKEN`
- **Tracked rooms** configured in `backend/config.py` `TRACKED_ROOMS` dict
- Frontend proxies to backend at `http://localhost:5000` (see package.json)
- Backend runs on port 5000, frontend on port 3000
