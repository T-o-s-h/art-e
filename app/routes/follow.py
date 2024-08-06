from flask import Blueprint, request, jsonify
from app import db
from app.models import User, Follow
from flask_jwt_extended import jwt_required, get_jwt_identity

bp = Blueprint('follow', __name__)

@bp.route('/follow/<int:artist_id>', methods=['POST'])
@jwt_required()
def follow_artist(artist_id):
    current_user_id = get_jwt_identity()
    artist = User.query.get_or_404(artist_id)
    if artist.is_artist and artist_id != current_user_id:
        follow_entry = Follow.query.filter_by(user_id=current_user_id, artist_id=artist_id).first()
        if follow_entry:
            return jsonify({'message': 'Already following this artist'}), 400
        new_follow = Follow(user_id=current_user_id, artist_id=artist_id)
        db.session.add(new_follow)
        db.session.commit()
        return jsonify({'message': 'Followed artist'}), 200
    return jsonify({'message': 'Invalid artist or self-following'}), 400

@bp.route('/unfollow/<int:artist_id>', methods=['POST'])
@jwt_required()
def unfollow_artist(artist_id):
    current_user_id = get_jwt_identity()
    follow_entry = Follow.query.filter_by(user_id=current_user_id, artist_id=artist_id).first_or_404()
    db.session.delete(follow_entry)
    db.session.commit()
    return jsonify({'message': 'Unfollowed artist'}), 200

@bp.route('/followers/<int:artist_id>', methods=['GET'])
def get_followers(artist_id):
    artist = User.query.get_or_404(artist_id)
    if not artist.is_artist:
        return jsonify({'message': 'User is not an artist'}), 400
    followers = Follow.query.filter_by(artist_id=artist_id).all()
    follower_ids = [follower.user_id for follower in followers]
    return jsonify({'followers': follower_ids}), 200

@bp.route('/following/<int:user_id>', methods=['GET'])
@jwt_required()
def get_following(user_id):
    current_user_id = get_jwt_identity()
    if current_user_id != user_id:
        return jsonify({'message': 'Unauthorized'}), 403
    following = Follow.query.filter_by(user_id=user_id).all()
    following_ids = [follow.artist_id for follow in following]
    return jsonify({'following': following_ids}), 200
