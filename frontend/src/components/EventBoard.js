import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { eventsAPI, syncAPI } from '../services/api';
import EventCard from './EventCard';
import EventModal from './EventModal';
import { format, parseISO, isToday, isTomorrow, isFuture, isPast } from 'date-fns';
import '../styles/EventBoard.css';

const EventBoard = () => {
  const { roomId } = useParams();
  const navigate = useNavigate();
  const [events, setEvents] = useState([]);
  const [filteredEvents, setFilteredEvents] = useState({ today: [], tomorrow: [], upcoming: [], past: [] });
  const [loading, setLoading] = useState(true);
  const [syncing, setSyncing] = useState(false);
  const [selectedEvent, setSelectedEvent] = useState(null);
  const [trackedRooms, setTrackedRooms] = useState({});

  useEffect(() => {
    fetchTrackedRooms();
  }, []);

  useEffect(() => {
    if (Object.keys(trackedRooms).length > 0) {
      fetchEvents();
    }
  }, [roomId, trackedRooms]);

  useEffect(() => {
    categorizeEvents();
  }, [events]);

  const fetchTrackedRooms = async () => {
    try {
      const response = await syncAPI.getTrackedRooms();
      setTrackedRooms(response.data);
    } catch (error) {
      console.error('Failed to fetch tracked rooms:', error);
    }
  };

  const fetchEvents = async () => {
    setLoading(true);
    try {
      const response = await eventsAPI.getEvents(roomId ? parseInt(roomId) : null);
      setEvents(response.data);
    } catch (error) {
      console.error('Failed to fetch events:', error);
    } finally {
      setLoading(false);
    }
  };

  const categorizeEvents = () => {
    const now = new Date();
    const categorized = {
      today: [],
      tomorrow: [],
      upcoming: [],
      past: [],
    };

    events.forEach((event) => {
      const eventDate = parseISO(event.event_start_date);

      if (isPast(eventDate) && !isToday(eventDate)) {
        categorized.past.push(event);
      } else if (isToday(eventDate)) {
        categorized.today.push(event);
      } else if (isTomorrow(eventDate)) {
        categorized.tomorrow.push(event);
      } else if (isFuture(eventDate)) {
        categorized.upcoming.push(event);
      }
    });

    setFilteredEvents(categorized);
  };

  const handleSync = async () => {
    setSyncing(true);
    try {
      await syncAPI.syncEvents();
      await fetchEvents();
      alert('Events synced successfully!');
    } catch (error) {
      console.error('Failed to sync events:', error);
      alert('Failed to sync events');
    } finally {
      setSyncing(false);
    }
  };

  const handleEventClick = (event) => {
    setSelectedEvent(event);
  };

  const handleCloseModal = () => {
    setSelectedEvent(null);
    fetchEvents(); // Refresh events after modal closes
  };

  const getRoomName = () => {
    if (!roomId) return 'All Rooms';
    return trackedRooms[roomId] || `Room ${roomId}`;
  };

  if (loading) {
    return <div className="loading">Loading events...</div>;
  }

  return (
    <div className="event-board">
      <div className="board-header">
        <div className="header-left">
          <h1>{getRoomName()}</h1>
          <select
            value={roomId || ''}
            onChange={(e) => navigate(e.target.value ? `/room/${e.target.value}` : '/')}
            className="room-selector"
          >
            <option value="">All Rooms</option>
            {Object.entries(trackedRooms).map(([id, name]) => (
              <option key={id} value={id}>
                {name}
              </option>
            ))}
          </select>
        </div>
        <button onClick={handleSync} disabled={syncing} className="btn-sync">
          {syncing ? 'Syncing...' : 'Sync Events'}
        </button>
      </div>

      <div className="board-columns">
        <div className="board-column">
          <h2>Today ({filteredEvents.today.length})</h2>
          <div className="events-list">
            {filteredEvents.today.map((event) => (
              <EventCard key={event.id} event={event} onClick={() => handleEventClick(event)} />
            ))}
            {filteredEvents.today.length === 0 && <p className="no-events">No events today</p>}
          </div>
        </div>

        <div className="board-column">
          <h2>Tomorrow ({filteredEvents.tomorrow.length})</h2>
          <div className="events-list">
            {filteredEvents.tomorrow.map((event) => (
              <EventCard key={event.id} event={event} onClick={() => handleEventClick(event)} />
            ))}
            {filteredEvents.tomorrow.length === 0 && <p className="no-events">No events tomorrow</p>}
          </div>
        </div>

        <div className="board-column">
          <h2>Upcoming ({filteredEvents.upcoming.length})</h2>
          <div className="events-list">
            {filteredEvents.upcoming.map((event) => (
              <EventCard key={event.id} event={event} onClick={() => handleEventClick(event)} />
            ))}
            {filteredEvents.upcoming.length === 0 && <p className="no-events">No upcoming events</p>}
          </div>
        </div>

        <div className="board-column">
          <h2>Past ({filteredEvents.past.length})</h2>
          <div className="events-list">
            {filteredEvents.past.slice(0, 10).map((event) => (
              <EventCard key={event.id} event={event} onClick={() => handleEventClick(event)} />
            ))}
            {filteredEvents.past.length === 0 && <p className="no-events">No past events</p>}
          </div>
        </div>
      </div>

      {selectedEvent && <EventModal event={selectedEvent} onClose={handleCloseModal} />}
    </div>
  );
};

export default EventBoard;
