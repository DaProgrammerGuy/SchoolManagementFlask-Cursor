from extensions import db

grade_subject = db.Table('grade_subject',
    db.Column('grade_id', db.Integer, db.ForeignKey('grade.id')),
    db.Column('subject_id', db.Integer, db.ForeignKey('subject.id'))
)

class Grade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    subjects = db.relationship("Subject", secondary=grade_subject, backref='grades')
    students = db.relationship('User', backref='grade') 