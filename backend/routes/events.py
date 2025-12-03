from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Event, EventNote, EventAssignment, User
from datetime import datetime

events_bp = Blueprint('events', __name__)


@events_bp.route('', methods=['GET'])
@jwt_required()
def get_events():
    """Get all events, optionally filtered by room_id"""
    room_id = request.args.get('room_id', type=int)

    query = Event.query

    if room_id:
        query = query.filter_by(room_id=room_id)

    # Filter out cancelled events by default
    include_cancelled = request.args.get('include_cancelled', 'false').lower() == 'true'
    if not include_cancelled:
        query = query.filter_by(cancelled=False)

    # Order by start date
    events = query.order_by(Event.event_start_date).all()

    return jsonify([event.to_dict() for event in events]), 200


@events_bp.route('/<int:event_id>', methods=['GET'])
@jwt_required()
def get_event(event_id):
    """Get a specific event"""
    event = Event.query.get(event_id)

    if not event:
        return jsonify({'error': 'Event not found'}), 404

    return jsonify(event.to_dict()), 200


@events_bp.route('/<int:event_id>/notes', methods=['POST'])
@jwt_required()
def add_note(event_id):
    """Add a note to an event"""
    user_id = get_jwt_identity()
    data = request.get_json()

    if not data or 'note' not in data:
        return jsonify({'error': 'Note text is required'}), 400

    event = Event.query.get(event_id)
    if not event:
        return jsonify({'error': 'Event not found'}), 404

    note = EventNote(
        event_id=event_id,
        user_id=user_id,
        note=data['note']
    )

    db.session.add(note)
    db.session.commit()

    return jsonify(note.to_dict()), 201


@events_bp.route('/<int:event_id>/notes/<int:note_id>', methods=['PUT'])
@jwt_required()
def update_note(event_id, note_id):
    """Update a note"""
    user_id = get_jwt_identity()
    data = request.get_json()

    note = EventNote.query.get(note_id)
    if not note or note.event_id != event_id:
        return jsonify({'error': 'Note not found'}), 404

    # Only the author can update the note
    if note.user_id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403

    if 'note' in data:
        note.note = data['note']
        note.updated_at = datetime.utcnow()

    db.session.commit()

    return jsonify(note.to_dict()), 200


@events_bp.route('/<int:event_id>/notes/<int:note_id>', methods=['DELETE'])
@jwt_required()
def delete_note(event_id, note_id):
    """Delete a note"""
    user_id = get_jwt_identity()

    note = EventNote.query.get(note_id)
    if not note or note.event_id != event_id:
        return jsonify({'error': 'Note not found'}), 404

    # Only the author can delete the note
    if note.user_id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403

    db.session.delete(note)
    db.session.commit()

    return jsonify({'message': 'Note deleted successfully'}), 200


@events_bp.route('/<int:event_id>/assignments', methods=['POST'])
@jwt_required()
def add_assignment(event_id):
    """Assign a user to an event"""
    data = request.get_json()

    if not data or 'user_id' not in data:
        return jsonify({'error': 'User ID is required'}), 400

    event = Event.query.get(event_id)
    if not event:
        return jsonify({'error': 'Event not found'}), 404

    user = User.query.get(data['user_id'])
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Check if assignment already exists
    existing = EventAssignment.query.filter_by(
        event_id=event_id,
        user_id=data['user_id']
    ).first()

    if existing:
        return jsonify({'error': 'User already assigned to this event'}), 409

    assignment = EventAssignment(
        event_id=event_id,
        user_id=data['user_id'],
        role=data.get('role', '')
    )

    db.session.add(assignment)
    db.session.commit()

    return jsonify(assignment.to_dict()), 201


@events_bp.route('/<int:event_id>/assignments/<int:assignment_id>', methods=['PUT'])
@jwt_required()
def update_assignment(event_id, assignment_id):
    """Update an assignment"""
    data = request.get_json()

    assignment = EventAssignment.query.get(assignment_id)
    if not assignment or assignment.event_id != event_id:
        return jsonify({'error': 'Assignment not found'}), 404

    if 'role' in data:
        assignment.role = data['role']

    db.session.commit()

    return jsonify(assignment.to_dict()), 200


@events_bp.route('/<int:event_id>/assignments/<int:assignment_id>', methods=['DELETE'])
@jwt_required()
def delete_assignment(event_id, assignment_id):
    """Remove an assignment"""
    assignment = EventAssignment.query.get(assignment_id)
    if not assignment or assignment.event_id != event_id:
        return jsonify({'error': 'Assignment not found'}), 404

    db.session.delete(assignment)
    db.session.commit()

    return jsonify({'message': 'Assignment removed successfully'}), 200
