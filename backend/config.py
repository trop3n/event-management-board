import os
from datetime import timedelta


class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://localhost/event_management'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key-change-in-production'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=8)

    # Ministry Platform API Configuration
    MP_API_URL = os.environ.get('MP_API_URL') or 'https://standrew.ministryplatform.com/ministryplatformapi/procs/api_church_specific_get_events'
    MP_BEARER_TOKEN = os.environ.get('MP_BEARER_TOKEN')

    # Room IDs for large event spaces
    TRACKED_ROOMS = {
        100: 'Sanctuary',
        128: 'Smith',
        131: 'Small Group Room 131',
        126: 'Small Group Room 126',
        120: 'Small Group Room 120',
        121: 'Small Group Room 121',
        122: 'Small Group Room 122',
        123: 'Small Group Room 123',
        124: 'Small Group Room 124',
        226: 'Movie Theater'
    }


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    SQLALCHEMY_ECHO = True


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
