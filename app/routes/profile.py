from flask import Blueprint, request, jsonify
from app import db
from app.models import ArtistProfile
from flask_jwt_extended import jwt_required, get_jwt_identity
import logging

# Initialize logger
logger = logging.getLogger(__name__)

# Define the blueprint for profile-related routes
bp = Blueprint('profile', __name__)

@bp.route('/profiles/<int:user_id>', methods=['GET'])
def get_profile(user_id):
    logger.info(f'Received GET request for profile of user_id: {user_id}')
    profile = ArtistProfile.query.filter_by(user_id=user_id).first_or_404()
    logger.info(f'Found profile: {profile}')
    return jsonify({
        'user_id': profile.user_id,
        'bio': profile.bio,
        'portfolio': profile.portfolio
    }), 200

@bp.route('/profiles/<int:user_id>', methods=['POST'])
@jwt_required()
def create_profile(user_id):
    logger.info(f'Received POST request to create profile for user_id: {user_id}')
    data = request.get_json()
    logger.info(f'Received data: {data}')
    current_user = get_jwt_identity()
    logger.info(f'Current user identity: {current_user}')
    if current_user != user_id:
        logger.warning(f'Unauthorized profile creation attempt by user: {current_user}')
        return jsonify({'message': 'Unauthorized'}), 403
    profile = ArtistProfile.query.filter_by(user_id=user_id).first()
    if profile:
        logger.warning(f'Profile already exists for user_id: {user_id}')
        return jsonify({'message': 'Profile already exists'}), 400
    new_profile = ArtistProfile(
        user_id=user_id,
        bio=data.get('bio'),
        portfolio=data.get('portfolio')
    )
    db.session.add(new_profile)
    db.session.commit()
    logger.info('Profile created successfully')
    return jsonify({'message': 'Profile created'}), 201

@bp.route('/profiles/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_profile(user_id):
    logger.info(f'Received PUT request to update profile for user_id: {user_id}')
    data = request.get_json()
    logger.info(f'Received data: {data}')
    current_user = get_jwt_identity()
    logger.info(f'Current user identity: {current_user}')
    if current_user != user_id:
        logger.warning(f'Unauthorized profile update attempt by user: {current_user}')
        return jsonify({'message': 'Unauthorized'}), 403
    profile = ArtistProfile.query.filter_by(user_id=user_id).first_or_404()
    logger.info(f'Found profile: {profile}')
    profile.bio = data.get('bio', profile.bio)
    profile.portfolio = data.get('portfolio', profile.portfolio)
    db.session.commit()
    logger.info('Profile updated successfully')
    return jsonify({'message': 'Profile updated'}), 200
