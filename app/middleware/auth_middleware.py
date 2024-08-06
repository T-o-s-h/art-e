from functools import wraps
from flask_jwt_extended import jwt_required, get_jwt_identity

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        current_user = get_jwt_identity()
        user = User.query.get(current_user)
        if user and user.is_admin:
            return fn(*args, **kwargs)
        else:
            return jsonify(message="Admin access required"), 403
    return wrapper
