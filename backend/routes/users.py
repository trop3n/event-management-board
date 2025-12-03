from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from models import User

users_bp = Blueprint('users', __name__)


@users_bp.route('', methods=['GET'])
@jwt_required()
def get_users():
    """Get all users"""
    users = User.query.all()
    return jsonify([user.to_dict() for user in users]), 200


@users_bp.route('/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    """Get a specific user"""
    user = User.query.get(user_id)

    if not user:
        return jsonify({'error': 'User not found'}), 404

    return jsonify(user.to_dict()), 200
