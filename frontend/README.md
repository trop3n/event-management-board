# Event Management Board - Frontend

React-based frontend for managing events from Ministry Platform.

## Features

- Kanban-style event organization (Today, Tomorrow, Upcoming, Past)
- Room-based filtering and navigation
- Event notes and collaboration
- Employee assignment to events
- Real-time event syncing

## Setup

1. Install dependencies:
```bash
npm install
```

2. Configure environment (optional):
```bash
cp .env.example .env
```

3. Start development server:
```bash
npm start
```

The app will open at http://localhost:3000

## Available Scripts

- `npm start` - Run development server
- `npm build` - Build for production
- `npm test` - Run tests

## Environment Variables

- `REACT_APP_API_URL` - Backend API URL (default: http://localhost:5000/api)
