from flask import jsonify
from models.grade import Grade
from models.subject import Subject
from models.user import User
from utils.serializers import serialize_grade, add_items_to_grade, add_items_to_grade2

def admin_grade_service(request, db):
    if request.method == "GET":
        gname = request.args.get('gname')
        if gname:
            grade = Grade.query.filter_by(name=gname).first()
            if not grade:
                return jsonify({"Message": "Grade not found"}), 404
            return serialize_grade(grade)
        else:
            grades = Grade.query.all()
            return jsonify({"Grades": [serialize_grade(g) for g in grades]})
    elif request.method == "POST":
        response = {}
        data = request.get_json()
        gname = data.get('name')
        if not gname:
            return jsonify({"Message": "Grade name required"}), 400
        grade = Grade.query.filter_by(name=gname).first()
        if not grade:
            grade = Grade(name=gname)
            db.session.add(grade)
            db.session.commit()
            response.setdefault('message', []).append(
                f"Grade with name {grade.name} has been added!")
        else:
            response.setdefault('warnings', []).append(
                f"Grade with name {grade.name} already exists!")
        if data.get('subjects'):
            warnings, added_items = add_items_to_grade('Subject', data['subjects'], grade,
                                                      'subjects', Subject, db)
            response['added subjects'] = added_items
            response.setdefault('warnings', []).extend(warnings)
            db.session.commit()
        if data.get('students'):
            warnings, added_items = add_items_to_grade2('Student', data['students'], grade,
                                                      'students', User, db)
            response['added students'] = added_items
            response.setdefault('warnings', []).extend(warnings)
            db.session.commit()
            for subject in grade.subjects:
                for student in grade.students:
                    if student not in subject.students:
                        subject.students.append(student)
            db.session.commit()
        return jsonify(response)
    return jsonify({"error": "Unhandled method"}), 405 