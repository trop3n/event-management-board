from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model):
    """User model for authentication and event assignment"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    event_assignments = db.relationship('EventAssignment', backref='user', lazy=True, cascade='all, delete-orphan')
    event_notes = db.relationship('EventNote', backref='author', lazy=True, cascade='all, delete-orphan')

    def set_password(self, password):
        """Hash and set the user's password"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verify the user's password"""
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        """Convert user object to dictionary"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'full_name': self.full_name,
            'created_at': self.created_at.isoformat()
        }


class Event(db.Model):
    """Event model from Ministry Platform"""
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, unique=True, nullable=False)  # Ministry Platform Event ID
    event_title = db.Column(db.String(200), nullable=False)
    event_type_id = db.Column(db.Integer)
    room_id = db.Column(db.Integer, nullable=False)
    room_name = db.Column(db.String(100))  # e.g., "Sanctuary", "Smith", etc.
    event_start_date = db.Column(db.DateTime, nullable=False)
    event_end_date = db.Column(db.DateTime, nullable=False)
    event_reservation_start = db.Column(db.DateTime)
    event_reservation_end = db.Column(db.DateTime)
    minutes_for_setup = db.Column(db.Integer, default=0)
    minutes_for_cleanup = db.Column(db.Integer, default=0)
    cancelled = db.Column(db.Boolean, default=False)
    approved = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    assignments = db.relationship('EventAssignment', backref='event', lazy=True, cascade='all, delete-orphan')
    notes = db.relationship('EventNote', backref='event', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        """Convert event object to dictionary"""
        return {
            'id': self.id,
            'event_id': self.event_id,
            'event_title': self.event_title,
            'event_type_id': self.event_type_id,
            'room_id': self.room_id,
            'room_name': self.room_name,
            'event_start_date': self.event_start_date.isoformat() if self.event_start_date else None,
            'event_end_date': self.event_end_date.isoformat() if self.event_end_date else None,
            'event_reservation_start': self.event_reservation_start.isoformat() if self.event_reservation_start else None,
            'event_reservation_end': self.event_reservation_end.isoformat() if self.event_reservation_end else None,
            'minutes_for_setup': self.minutes_for_setup,
            'minutes_for_cleanup': self.minutes_for_cleanup,
            'cancelled': self.cancelled,
            'approved': self.approved,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'assignments': [a.to_dict() for a in self.assignments],
            'notes': [n.to_dict() for n in self.notes]
        }


class EventAssignment(db.Model):
    """Assignment of employees to events"""
    __tablename__ = 'event_assignments'

    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    role = db.Column(db.String(100))  # e.g., "Tech Lead", "Audio", "Video", etc.
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        """Convert assignment object to dictionary"""
        return {
            'id': self.id,
            'event_id': self.event_id,
            'user': self.user.to_dict() if self.user else None,
            'role': self.role,
            'created_at': self.created_at.isoformat()
        }


class EventNote(db.Model):
    """Notes for events"""
    __tablename__ = 'event_notes'

    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    note = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        """Convert note object to dictionary"""
        return {
            'id': self.id,
            'event_id': self.event_id,
            'author': self.author.to_dict() if self.author else None,
            'note': self.note,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
