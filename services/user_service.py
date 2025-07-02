from flask import jsonify, make_response, request
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
from models.user import User
from models.grade import Grade
from models.subject import Subject
from utils.serializers import serialize_student, serialize_teacher, add_items_to_user

def create_user_service(data, db):
    username = data['username']
    email = data.get('email')
    password = generate_password_hash(data['password'], 'pbkdf2:sha256')
    role = data['role'].lower()
    if role not in ['student', 'teacher', 'admin']:
        return jsonify({"Message": "Invalid role"}), 400
    if not email:
        return jsonify({"Message": "Email is required"}), 400
    user = User(username=username, email=email, password=password, role=role)
    db.session.add(user)
    db.session.commit()
    return jsonify({"Message": f"New {role} user '{username}' has been created"}), 201

def login_service(data, db):
    username = data.get('username')
    password = data.get('password')
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"Message": "No such user found!"}), 404
    if check_password_hash(user.password, password):
        token = jwt.encode({
            "user": username,
            "role": user.role,
            "exp": datetime.utcnow() + timedelta(minutes=30)
        }, db.app.config["SECRET_KEY"], algorithm="HS256")
        response = make_response(jsonify({"Message": f"User {username} logged in", "Token": token}))
        response.set_cookie("JWT", token)
        return response
    else:
        return jsonify({"Message": "Could not verify!"}), 401

def admin_user_service(request, db):
    if request.method == 'GET':
        user_name = request.args.get('username')
        if user_name:
            user = User.query.filter_by(username=user_name).first()
            if not user:
                return jsonify({"Message": "User not found"})
            if user.role == 'teacher':
                return serialize_teacher(user)
            elif user.role == 'student':
                return serialize_student(user)
        else:
            user_role = request.args.get('role')
            users = User.query.filter_by(role=user_role).all()
            if not users:
                return jsonify({"Message": "User not found"})
            if user_role == 'teacher':
                return [serialize_teacher(u) for u in users]
            elif user_role == 'student':
                return [serialize_student(u) for u in users]
    elif request.method == 'POST':
        response = {}
        data = request.get_json()
        role = data.get('role')
        username = data.get('username')
        password = data.get('password')
        user = User.query.filter_by(username=username, role=role).first()
        if not user:
            user = User(username=username, role=role,
                           password=generate_password_hash(password, 'pbkdf2:sha256'))
            db.session.add(user)
            db.session.commit()
            response.setdefault('message', []).append(
                f"User with role {user.role} and username {user.username} has been added!")
        else:
            response.setdefault("warnings", []).append(
                f"User with role {user.role} and username {user.username} already exists!")
        if role == 'teacher':
            if data.get('grades'):
                warnings, added_items = add_items_to_user('Grade', data['grades'], user,
                                                          'teacher_grades', Grade, db)
                response['added grades'] = added_items
                response.setdefault('warnings', []).extend(warnings)
                db.session.commit()
            if data.get('subjects'):
                warnings, added_items = add_items_to_user('Subject', data['subjects'], user,
                                                          'teacher_subjects', Subject, db)
                response['added subjects'] = added_items
                response.setdefault('warnings', []).extend(warnings)
                db.session.commit()
            for grade in user.teacher_grades:
                for subject in user.teacher_subjects:
                    if subject not in grade.subjects:
                        grade.subjects.append(subject)
            db.session.commit()
            return jsonify(response)
        elif role == 'student':
            if data.get('grade'):
                warnings, added_items = add_items_to_user('Grade', data['grade'], user,
                                                          'grade', Grade, db)
                response['added grades'] = added_items
                response.setdefault('warnings', []).extend(warnings)
                db.session.commit()
            if data.get('subjects'):
                warnings, added_items = add_items_to_user('Subject', data['subjects'], user,
                                                                  'student_subjects', Subject, db)
                response['added subjects'] = added_items
                response.setdefault('warnings', []).extend(warnings)
                db.session.commit()
            if user.grade:
                for subject in user.student_subjects:
                    if subject not in user.grade.subjects:
                        user.grade.subjects.append(subject)
            db.session.commit()
            return jsonify(response)
    return jsonify({"error": "Unhandled method"}), 405 