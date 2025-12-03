import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Auth API
export const authAPI = {
  register: (userData) => api.post('/auth/register', userData),
  login: (credentials) => api.post('/auth/login', credentials),
  getCurrentUser: () => api.get('/auth/me'),
};

// Events API
export const eventsAPI = {
  getEvents: (roomId = null) => {
    const params = roomId ? { room_id: roomId } : {};
    return api.get('/events', { params });
  },
  getEvent: (id) => api.get(`/events/${id}`),
  addNote: (eventId, note) => api.post(`/events/${eventId}/notes`, { note }),
  updateNote: (eventId, noteId, note) => api.put(`/events/${eventId}/notes/${noteId}`, { note }),
  deleteNote: (eventId, noteId) => api.delete(`/events/${eventId}/notes/${noteId}`),
  addAssignment: (eventId, userId, role) => api.post(`/events/${eventId}/assignments`, { user_id: userId, role }),
  updateAssignment: (eventId, assignmentId, role) => api.put(`/events/${eventId}/assignments/${assignmentId}`, { role }),
  deleteAssignment: (eventId, assignmentId) => api.delete(`/events/${eventId}/assignments/${assignmentId}`),
};

// Sync API
export const syncAPI = {
  syncEvents: () => api.post('/sync/events'),
  getTrackedRooms: () => api.get('/sync/rooms'),
};

// Users API
export const usersAPI = {
  getUsers: () => api.get('/users'),
  getUser: (id) => api.get(`/users/${id}`),
};

export default api;
