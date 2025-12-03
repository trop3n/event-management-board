import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './services/AuthContext';
import Login from './components/Login';
import EventBoard from './components/EventBoard';
import './styles/App.css';

const PrivateRoute = ({ children }) => {
  const { user, loading } = useAuth();

  if (loading) {
    return <div className="loading">Loading...</div>;
  }

  return user ? children : <Navigate to="/login" />;
};

const AppLayout = () => {
  const { user, logout } = useAuth();

  return (
    <div className="app">
      {user && (
        <nav className="navbar">
          <div className="nav-brand">Event Management Board</div>
          <div className="nav-user">
            <span>Welcome, {user.full_name}</span>
            <button onClick={logout} className="btn-logout">
              Logout
            </button>
          </div>
        </nav>
      )}
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route
          path="/"
          element={
            <PrivateRoute>
              <EventBoard />
            </PrivateRoute>
          }
        />
        <Route
          path="/room/:roomId"
          element={
            <PrivateRoute>
              <EventBoard />
            </PrivateRoute>
          }
        />
      </Routes>
    </div>
  );
};

function App() {
  return (
    <Router>
      <AuthProvider>
        <AppLayout />
      </AuthProvider>
    </Router>
  );
}

export default App;
