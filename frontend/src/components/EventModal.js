import React, { useState, useEffect } from 'react';
import { format, parseISO } from 'date-fns';
import { eventsAPI, usersAPI } from '../services/api';
import { useAuth } from '../services/AuthContext';
import '../styles/EventModal.css';

const EventModal = ({ event, onClose }) => {
  const { user } = useAuth();
  const [notes, setNotes] = useState(event.notes || []);
  const [assignments, setAssignments] = useState(event.assignments || []);
  const [newNote, setNewNote] = useState('');
  const [users, setUsers] = useState([]);
  const [selectedUserId, setSelectedUserId] = useState('');
  const [selectedRole, setSelectedRole] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchUsers();
  }, []);

  const fetchUsers = async () => {
    try {
      const response = await usersAPI.getUsers();
      setUsers(response.data);
    } catch (error) {
      console.error('Failed to fetch users:', error);
    }
  };

  const handleAddNote = async (e) => {
    e.preventDefault();
    if (!newNote.trim()) return;

    setLoading(true);
    try {
      const response = await eventsAPI.addNote(event.id, newNote);
      setNotes([...notes, response.data]);
      setNewNote('');
    } catch (error) {
      console.error('Failed to add note:', error);
      alert('Failed to add note');
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteNote = async (noteId) => {
    if (!window.confirm('Delete this note?')) return;

    try {
      await eventsAPI.deleteNote(event.id, noteId);
      setNotes(notes.filter((n) => n.id !== noteId));
    } catch (error) {
      console.error('Failed to delete note:', error);
      alert('Failed to delete note');
    }
  };

  const handleAddAssignment = async (e) => {
    e.preventDefault();
    if (!selectedUserId) return;

    setLoading(true);
    try {
      const response = await eventsAPI.addAssignment(event.id, parseInt(selectedUserId), selectedRole);
      setAssignments([...assignments, response.data]);
      setSelectedUserId('');
      setSelectedRole('');
    } catch (error) {
      console.error('Failed to add assignment:', error);
      alert(error.response?.data?.error || 'Failed to add assignment');
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteAssignment = async (assignmentId) => {
    if (!window.confirm('Remove this assignment?')) return;

    try {
      await eventsAPI.deleteAssignment(event.id, assignmentId);
      setAssignments(assignments.filter((a) => a.id !== assignmentId));
    } catch (error) {
      console.error('Failed to delete assignment:', error);
      alert('Failed to remove assignment');
    }
  };

  const formatDateTime = (dateString) => {
    if (!dateString) return '';
    return format(parseISO(dateString), 'MMM d, yyyy h:mm a');
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>{event.event_title}</h2>
          <button className="modal-close" onClick={onClose}>
            ×
          </button>
        </div>

        <div className="modal-body">
          <div className="event-info">
            <div className="info-row">
              <strong>Room:</strong> {event.room_name}
            </div>
            <div className="info-row">
              <strong>Event Time:</strong> {formatDateTime(event.event_start_date)} - {format(parseISO(event.event_end_date), 'h:mm a')}
            </div>
            {event.event_reservation_start && (
              <div className="info-row">
                <strong>Reserved:</strong> {formatDateTime(event.event_reservation_start)} - {format(parseISO(event.event_reservation_end), 'h:mm a')}
              </div>
            )}
            {event.minutes_for_setup > 0 && (
              <div className="info-row">
                <strong>Setup Time:</strong> {event.minutes_for_setup} minutes
              </div>
            )}
            {event.minutes_for_cleanup > 0 && (
              <div className="info-row">
                <strong>Cleanup Time:</strong> {event.minutes_for_cleanup} minutes
              </div>
            )}
            {event.cancelled && (
              <div className="info-row">
                <span className="badge cancelled">Event Cancelled</span>
              </div>
            )}
          </div>

          <div className="section">
            <h3>Assignments</h3>
            <div className="assignments-list">
              {assignments.length === 0 && <p className="no-items">No assignments yet</p>}
              {assignments.map((assignment) => (
                <div key={assignment.id} className="assignment-item">
                  <div>
                    <strong>{assignment.user?.full_name}</strong>
                    {assignment.role && <span className="role"> - {assignment.role}</span>}
                  </div>
                  <button onClick={() => handleDeleteAssignment(assignment.id)} className="btn-delete">
                    Remove
                  </button>
                </div>
              ))}
            </div>

            <form onSubmit={handleAddAssignment} className="add-assignment-form">
              <select
                value={selectedUserId}
                onChange={(e) => setSelectedUserId(e.target.value)}
                required
              >
                <option value="">Select employee...</option>
                {users.map((u) => (
                  <option key={u.id} value={u.id}>
                    {u.full_name}
                  </option>
                ))}
              </select>
              <input
                type="text"
                placeholder="Role (optional)"
                value={selectedRole}
                onChange={(e) => setSelectedRole(e.target.value)}
              />
              <button type="submit" disabled={loading || !selectedUserId} className="btn-primary">
                Assign
              </button>
            </form>
          </div>

          <div className="section">
            <h3>Notes</h3>
            <div className="notes-list">
              {notes.length === 0 && <p className="no-items">No notes yet</p>}
              {notes.map((note) => (
                <div key={note.id} className="note-item">
                  <div className="note-header">
                    <strong>{note.author?.full_name}</strong>
                    <span className="note-date">{format(parseISO(note.created_at), 'MMM d, h:mm a')}</span>
                  </div>
                  <p className="note-text">{note.note}</p>
                  {note.author?.id === user?.id && (
                    <button onClick={() => handleDeleteNote(note.id)} className="btn-delete-note">
                      Delete
                    </button>
                  )}
                </div>
              ))}
            </div>

            <form onSubmit={handleAddNote} className="add-note-form">
              <textarea
                placeholder="Add a note..."
                value={newNote}
                onChange={(e) => setNewNote(e.target.value)}
                rows="3"
                required
              />
              <button type="submit" disabled={loading || !newNote.trim()} className="btn-primary">
                Add Note
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
};

export default EventModal;
