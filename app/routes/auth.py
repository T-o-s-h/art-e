from flask import Blueprint, request, jsonify
from app import db
from app.models import User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

bp = Blueprint('auth', __name__)

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    is_artist = data.get('is_artist', False)
    
    user = User(username=username, email=email, is_artist=is_artist)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    
    return jsonify(message="User registered successfully"), 201

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify(message="Invalid credentials"), 401

@bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    current_user = get_jwt_identity()
    user = User.query.get(current_user)
    
    return jsonify({
        'username': user.username,
        'email': user.email,
        'is_artist': user.is_artist
    })

# Add the following routes if you want to include password management and token refresh functionality

@bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)
    return jsonify(access_token=access_token), 200

@bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    # Here, you might want to add logic to invalidate the token, but Flask-JWT-Extended doesn't handle token revocation out-of-the-box
    return jsonify(message="Logout successful"), 200
