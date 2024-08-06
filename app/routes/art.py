from flask import Blueprint, request, jsonify
from app import db
from app.models import Artwork
from flask_jwt_extended import jwt_required

bp = Blueprint('art', __name__)

@bp.route('/artworks', methods=['POST'])
def create_artwork():
    data = request.get_json()
    new_artwork = Artwork(
        title=data['title'],
        description=data.get('description'),
        price=data['price'],
        artist_id=data['artist_id']
    )
    db.session.add(new_artwork)
    db.session.commit()
    return jsonify({'message': 'Artwork created'}), 201

@bp.route('/artworks/<int:id>', methods=['GET'])
def get_artwork(id):
    artwork = Artwork.query.get_or_404(id)
    return jsonify({
        'id': artwork.id,
        'title': artwork.title,
        'description': artwork.description,
        'price': artwork.price,
        'artist_id': artwork.artist_id
    })

@bp.route('/artworks/<int:id>', methods=['PUT'])
def update_artwork(id):
    data = request.get_json()
    artwork = Artwork.query.get_or_404(id)
    artwork.title = data['title']
    artwork.description = data.get('description')
    artwork.price = data['price']
    artwork.artist_id = data['artist_id']
    db.session.commit()
    return jsonify({'message': 'Artwork updated'})

@bp.route('/artworks/<int:id>', methods=['DELETE'])
def delete_artwork(id):
    artwork = Artwork.query.get_or_404(id)
    db.session.delete(artwork)
    db.session.commit()
    return jsonify({'message': 'Artwork deleted'})
