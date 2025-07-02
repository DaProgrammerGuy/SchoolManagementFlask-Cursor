from flask import request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
from models.user import User
from utils.serializers import serialize_student, serialize_teacher
from utils.decorators import token_required
from services.user_service import create_user_service, login_service

def register_auth_routes(app, db):
    @app.route('/user', methods=["POST"])
    def create_user():
        data = request.get_json()
        return create_user_service(data, db)

    @app.route('/login', methods=['POST'])
    def login():
        data = request.get_json()
        return login_service(data, db) 