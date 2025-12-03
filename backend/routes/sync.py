from flask import Blueprint, jsonify, current_app
from flask_jwt_extended import jwt_required
from models import db, Event
from datetime import datetime, timedelta
import requests

sync_bp = Blueprint('sync', __name__)


def fetch_events_from_mp(start_date, end_date):
    """Fetch events from Ministry Platform API"""
    url = current_app.config['MP_API_URL']
    bearer_token = current_app.config['MP_BEARER_TOKEN']

    if not bearer_token:
        raise ValueError('MP_BEARER_TOKEN not configured')

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {bearer_token}'
    }

    payload = {
        "@StartDate": start_date.strftime('%m/%d/%Y'),
        "@EndDate": end_date.strftime('%m/%d/%Y')
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()

    return response.json()


def sync_events_to_db(events_data, tracked_rooms):
    """Sync events to database, filtering by tracked room IDs"""
    synced_count = 0
    updated_count = 0

    # Flatten the nested array structure from MP API
    if events_data and isinstance(events_data[0], list):
        events_data = events_data[0]

    for event_data in events_data:
        room_id = event_data.get('Room_ID')

        # Only sync events for tracked rooms
        if room_id not in tracked_rooms:
            continue

        event_id = event_data.get('Event_Room_ID')  # Using Event_Room_ID as unique identifier

        # Check if event already exists
        event = Event.query.filter_by(event_id=event_id).first()

        if event:
            # Update existing event
            event.event_title = event_data.get('Event_Title', '')
            event.event_type_id = event_data.get('Event_Type_ID')
            event.room_id = room_id
            event.room_name = tracked_rooms.get(room_id, f'Room {room_id}')
            event.event_start_date = datetime.fromisoformat(event_data.get('Event_Start_Date').replace('Z', '+00:00')) if event_data.get('Event_Start_Date') else None
            event.event_end_date = datetime.fromisoformat(event_data.get('Event_End_Date').replace('Z', '+00:00')) if event_data.get('Event_End_Date') else None
            event.event_reservation_start = datetime.fromisoformat(event_data.get('Event_Reservation_Start').replace('Z', '+00:00')) if event_data.get('Event_Reservation_Start') else None
            event.event_reservation_end = datetime.fromisoformat(event_data.get('Event_Reservation_End').replace('Z', '+00:00')) if event_data.get('Event_Reservation_End') else None
            event.minutes_for_setup = event_data.get('Minutes_for_Setup', 0)
            event.minutes_for_cleanup = event_data.get('Minutes_for_Cleanup', 0)
            event.cancelled = event_data.get('Cancelled', False)
            event.approved = event_data.get('_Approved', False)
            event.updated_at = datetime.utcnow()
            updated_count += 1
        else:
            # Create new event
            event = Event(
                event_id=event_id,
                event_title=event_data.get('Event_Title', ''),
                event_type_id=event_data.get('Event_Type_ID'),
                room_id=room_id,
                room_name=tracked_rooms.get(room_id, f'Room {room_id}'),
                event_start_date=datetime.fromisoformat(event_data.get('Event_Start_Date').replace('Z', '+00:00')) if event_data.get('Event_Start_Date') else None,
                event_end_date=datetime.fromisoformat(event_data.get('Event_End_Date').replace('Z', '+00:00')) if event_data.get('Event_End_Date') else None,
                event_reservation_start=datetime.fromisoformat(event_data.get('Event_Reservation_Start').replace('Z', '+00:00')) if event_data.get('Event_Reservation_Start') else None,
                event_reservation_end=datetime.fromisoformat(event_data.get('Event_Reservation_End').replace('Z', '+00:00')) if event_data.get('Event_Reservation_End') else None,
                minutes_for_setup=event_data.get('Minutes_for_Setup', 0),
                minutes_for_cleanup=event_data.get('Minutes_for_Cleanup', 0),
                cancelled=event_data.get('Cancelled', False),
                approved=event_data.get('_Approved', False)
            )
            db.session.add(event)
            synced_count += 1

    db.session.commit()
    return synced_count, updated_count


@sync_bp.route('/events', methods=['POST'])
@jwt_required()
def sync_events():
    """Sync events from Ministry Platform API"""
    try:
        # Default to next 30 days
        start_date = datetime.now()
        end_date = start_date + timedelta(days=30)

        # Fetch events from Ministry Platform
        events_data = fetch_events_from_mp(start_date, end_date)

        # Sync to database with room filtering
        tracked_rooms = current_app.config['TRACKED_ROOMS']
        synced_count, updated_count = sync_events_to_db(events_data, tracked_rooms)

        return jsonify({
            'message': 'Events synced successfully',
            'synced': synced_count,
            'updated': updated_count,
            'total': synced_count + updated_count
        }), 200

    except requests.RequestException as e:
        return jsonify({'error': f'Failed to fetch events from Ministry Platform: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Sync failed: {str(e)}'}), 500


@sync_bp.route('/rooms', methods=['GET'])
@jwt_required()
def get_tracked_rooms():
    """Get list of tracked rooms"""
    tracked_rooms = current_app.config['TRACKED_ROOMS']
    return jsonify(tracked_rooms), 200
