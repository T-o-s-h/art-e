from flask import Blueprint, request, jsonify
from app import db
from app.models import Artwork
from flask_jwt_extended import jwt_required, get_jwt_identity

bp = Blueprint('artworks', __name__, url_prefix='/artworks')

@bp.route('', methods=['POST'])
@jwt_required()
def create_artwork():
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    price = data.get('price')
    
    if not title or not price:
        return jsonify(message="Title and price are required"), 400

    artist_id = get_jwt_identity()  # assuming the artist is the currently authenticated user
    
    artwork = Artwork(title=title, description=description, price=price, artist_id=artist_id)
    db.session.add(artwork)
    db.session.commit()

    return jsonify(message="Artwork created successfully"), 201

@bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_artwork(id):
    data = request.get_json()
    artwork = Artwork.query.get_or_404(id)
    
    if artwork.artist_id != get_jwt_identity():
        return jsonify(message="Unauthorized"), 403

    artwork.title = data.get('title', artwork.title)
    artwork.description = data.get('description', artwork.description)
    artwork.price = data.get('price', artwork.price)
    
    db.session.commit()

    return jsonify(message="Artwork updated successfully")

@bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_artwork(id):
    artwork = Artwork.query.get_or_404(id)
    
    if artwork.artist_id != get_jwt_identity():
        return jsonify(message="Unauthorized"), 403

    db.session.delete(artwork)
    db.session.commit()

    return jsonify(message="Artwork deleted successfully")

@bp.route('/<int:id>', methods=['GET'])
def get_artwork(id):
    artwork = Artwork.query.get_or_404(id)
    return jsonify({
        'id': artwork.id,
        'title': artwork.title,
        'description': artwork.description,
        'price': artwork.price,
        'artist_id': artwork.artist_id
    })
