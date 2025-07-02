from functools import wraps
from flask import request, jsonify
import jwt
from models.user import User

def token_role_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        from app import app
        token = request.headers.get("Authorization", "").removeprefix("Bearer ").strip()

        if not token:
            return jsonify({"Message": "Token Missing!"})

        try:
            data = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
        except:
            return jsonify({"Message": "Invalid Token!"}), 403

        if data.get("role") != 'admin':
            return jsonify({"Message": "Unauthorized"}), 403

        return f(*args, **kwargs)
    return wrapper

def token_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        from app import app
        token = request.headers.get("Authorization", "").removeprefix("Bearer ").strip()

        if not token:
            return jsonify({"Message": "Token Missing!"})

        try:
            data = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
            username = data.get("user")
            current_user = User.query.filter_by(username=username).first()
            if not current_user:
                return jsonify({"Message": "User not found!"}), 404
        except:
            return jsonify({"Message": "Invalid Token!"}), 403

        return f(current_user, *args, **kwargs)
    return wrapper 