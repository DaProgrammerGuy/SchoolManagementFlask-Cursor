from extensions import db

teacher_grade = db.Table('teacher_grade',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('grade_id', db.Integer, db.ForeignKey('grade.id'))
)

teacher_subject = db.Table('teacher_subject',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('subject_id', db.Integer, db.ForeignKey('subject.id'))
)

student_subject = db.Table('student_subject',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('subject_id', db.Integer, db.ForeignKey('subject.id'))
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    role = db.Column(db.String(10))  # 'student', 'teacher', 'admin'
    grade_id = db.Column(db.Integer, db.ForeignKey('grade.id'), nullable=True)
    teacher_grades = db.relationship("Grade", secondary=teacher_grade, backref='teachers')
    teacher_subjects = db.relationship("Subject", secondary=teacher_subject, backref='teachers')
    student_subjects = db.relationship("Subject", secondary=student_subject, backref='students') 