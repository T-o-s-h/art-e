from flask import Blueprint, request, jsonify
from app import db
from app.models import ArtistProfile
from flask_jwt_extended import jwt_required, get_jwt_identity

bp = Blueprint('artist_profile', __name__, url_prefix='/profile')

@bp.route('', methods=['POST'])
@jwt_required()
def create_profile():
    data = request.get_json()
    bio = data.get('bio')
    portfolio_url = data.get('portfolio_url')
    
    user_id = get_jwt_identity()

    profile = ArtistProfile(user_id=user_id, bio=bio, portfolio_url=portfolio_url)
    db.session.add(profile)
    db.session.commit()

    return jsonify(message="Profile created successfully"), 201

@bp.route('', methods=['PUT'])
@jwt_required()
def update_profile():
    data = request.get_json()
    profile = ArtistProfile.query.filter_by(user_id=get_jwt_identity()).first_or_404()
    
    profile.bio = data.get('bio', profile.bio)
    profile.portfolio_url = data.get('portfolio_url', profile.portfolio_url)
    
    db.session.commit()

    return jsonify(message="Profile updated successfully")

@bp.route('', methods=['GET'])
@jwt_required()  # Added JWT requirement for GET as well
def get_profile():
    profile = ArtistProfile.query.filter_by(user_id=get_jwt_identity()).first_or_404()
    return jsonify({
        'bio': profile.bio,
        'portfolio_url': profile.portfolio_url
    })
