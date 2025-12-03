from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from models import db
from config import config
import os

# Import routes
from routes.auth import auth_bp
from routes.events import events_bp
from routes.users import users_bp
from routes.sync import sync_bp


def create_app(config_name='default'):
    """Application factory"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Initialize extensions
    db.init_app(app)
    CORS(app)
    JWTManager(app)

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(events_bp, url_prefix='/api/events')
    app.register_blueprint(users_bp, url_prefix='/api/users')
    app.register_blueprint(sync_bp, url_prefix='/api/sync')

    # Create tables
    with app.app_context():
        db.create_all()

    return app


if __name__ == '__main__':
    env = os.environ.get('FLASK_ENV', 'development')
    app = create_app(env)
    app.run(host='0.0.0.0', port=5000, debug=True)
