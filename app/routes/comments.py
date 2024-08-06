from flask import Blueprint, request, jsonify
from app import db
from app.models import Comment
from flask_jwt_extended import jwt_required, get_jwt_identity

bp = Blueprint('comments', __name__)

@bp.route('/comments', methods=['POST'])
@jwt_required()
def create_comment():
    data = request.get_json()
    new_comment = Comment(
        content=data['content'],
        user_id=get_jwt_identity(),
        artwork_id=data.get('artwork_id')  # Assuming you're associating comments with artworks
    )
    db.session.add(new_comment)
    db.session.commit()
    return jsonify({'message': 'Comment created'}), 201

@bp.route('/comments/<int:id>', methods=['GET'])
def get_comment(id):
    comment = Comment.query.get_or_404(id)
    return jsonify({
        'id': comment.id,
        'content': comment.content,
        'user_id': comment.user_id,
        'artwork_id': comment.artwork_id  # Include artwork ID if needed
    })

@bp.route('/comments/<int:id>', methods=['PUT'])
@jwt_required()
def update_comment(id):
    data = request.get_json()
    comment = Comment.query.get_or_404(id)
    if comment.user_id != get_jwt_identity():
        return jsonify({'message': 'Unauthorized'}), 403
    
    comment.content = data.get('content', comment.content)
    db.session.commit()
    return jsonify({'message': 'Comment updated'})

@bp.route('/comments/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_comment(id):
    comment = Comment.query.get_or_404(id)
    if comment.user_id != get_jwt_identity():
        return jsonify({'message': 'Unauthorized'}), 403
    db.session.delete(comment)
    db.session.commit()
    return jsonify({'message': 'Comment deleted'})

@bp.route('/comments/artwork/<int:artwork_id>', methods=['GET'])
def get_comments_by_artwork(artwork_id):
    comments = Comment.query.filter_by(artwork_id=artwork_id).all()
    return jsonify([
        {
            'id': comment.id,
            'content': comment.content,
            'user_id': comment.user_id
        } for comment in comments
    ])
