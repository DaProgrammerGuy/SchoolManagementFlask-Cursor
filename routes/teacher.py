from flask import jsonify
from utils.decorators import token_required

def register_teacher_routes(app, db):
    @app.route('/teacher/dashboard', methods=["GET"])
    @token_required
    def teacher_dashboard(current_user):
        if current_user.role != 'teacher':
            return jsonify({"Message": "Access denied. Only teachers allowed."}), 403
        return jsonify({
            "username": current_user.username,
            "grades": [grade.name for grade in current_user.teacher_grades],
            "subjects": [subject.name for subject in current_user.teacher_subjects]
        }) 