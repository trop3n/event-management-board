import React from 'react';
import { format, parseISO } from 'date-fns';
import '../styles/EventCard.css';

const EventCard = ({ event, onClick }) => {
  const formatTime = (dateString) => {
    if (!dateString) return '';
    return format(parseISO(dateString), 'h:mm a');
  };

  const formatDate = (dateString) => {
    if (!dateString) return '';
    return format(parseISO(dateString), 'MMM d, yyyy');
  };

  const getAssignmentSummary = () => {
    if (!event.assignments || event.assignments.length === 0) {
      return 'No assignments';
    }
    if (event.assignments.length === 1) {
      return `1 person assigned`;
    }
    return `${event.assignments.length} people assigned`;
  };

  const getNotesSummary = () => {
    if (!event.notes || event.notes.length === 0) {
      return '';
    }
    if (event.notes.length === 1) {
      return '1 note';
    }
    return `${event.notes.length} notes`;
  };

  return (
    <div className={`event-card ${event.cancelled ? 'cancelled' : ''}`} onClick={onClick}>
      <div className="event-header">
        <h3>{event.event_title}</h3>
        {event.cancelled && <span className="badge cancelled">Cancelled</span>}
      </div>

      <div className="event-details">
        <div className="event-time">
          <span className="time-label">Event:</span>
          <span>{formatTime(event.event_start_date)} - {formatTime(event.event_end_date)}</span>
        </div>

        {event.event_reservation_start && (
          <div className="event-time reservation">
            <span className="time-label">Reserved:</span>
            <span>{formatTime(event.event_reservation_start)} - {formatTime(event.event_reservation_end)}</span>
          </div>
        )}

        <div className="event-room">
          <span className="room-label">Room:</span>
          <span>{event.room_name}</span>
        </div>
      </div>

      <div className="event-footer">
        <span className="assignment-summary">{getAssignmentSummary()}</span>
        {getNotesSummary() && <span className="notes-summary">{getNotesSummary()}</span>}
      </div>
    </div>
  );
};

export default EventCard;
