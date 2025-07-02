from flask import jsonify
from models.subject import Subject
from models.grade import Grade
from models.user import User
from utils.serializers import serialize_subject, add_items_to_grade, add_items_to_grade2

def admin_subject_service(request, db):
    if request.method == "GET":
        sname = request.args.get('sname')
        if sname:
            subject = Subject.query.filter_by(name=sname).first()
            if not subject:
                return jsonify({"Message": "Subject not found"}), 404
            return serialize_subject(subject)
        else:
            subjects = Subject.query.all()
            return jsonify({"Subjects": [serialize_subject(s) for s in subjects]})
    elif request.method == "POST":
        response = {}
        data = request.get_json()
        sname = data.get('name')
        if not sname:
            return jsonify({"Message": "Subject name required"}), 400
        subject = Subject.query.filter_by(name=sname).first()
        if not subject:
            subject = Subject(name=sname)
            db.session.add(subject)
            db.session.commit()
            response.setdefault('message', []).append(
                f"Subject with name {subject.name} has been added!")
        else:
            response.setdefault('warnings', []).append(
                f"Subject with name {subject.name} already exists!")
        if data.get('grades'):
            warnings, added_items = add_items_to_grade('Grade', data['grades'], subject,
                                                      'grades', Grade, db)
            response['added grades'] = added_items
            response.setdefault('warnings', []).extend(warnings)
            db.session.commit()
        if data.get('teacher'):
            warnings, added_items = add_items_to_grade2('Teacher', data['teacher'], subject,
                                                      'teachers', User, db)
            response['added teachers'] = added_items
            response.setdefault('warnings', []).extend(warnings)
            db.session.commit()
            for grade in subject.grades:
                for teacher in subject.teachers:
                    if teacher not in grade.teachers:
                        grade.teachers.append(teacher)
            db.session.commit()
        return jsonify(response)
    return jsonify({"error": "Unhandled method"}), 405 