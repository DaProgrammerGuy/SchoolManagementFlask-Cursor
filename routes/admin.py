from flask import request, jsonify
from utils.decorators import token_role_required
from services.user_service import admin_user_service
from services.grade_service import admin_grade_service
from services.subject_service import admin_subject_service

def register_admin_routes(app, db):
    @app.route('/admin/user', methods=['GET', 'POST'])
    @token_role_required
    def admin_user():
        return admin_user_service(request, db)

    @app.route('/admin/grade', methods=['GET', 'POST'])
    @token_role_required
    def admin_grade():
        return admin_grade_service(request, db)

    @app.route('/admin/subject', methods=['GET', 'POST'])
    @token_role_required
    def admin_subject():
        return admin_subject_service(request, db) 