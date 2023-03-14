from flask import Flask, request, session
from flask_sqlalchemy import SQLAlchemy

# create the extension
db = SQLAlchemy()

app = Flask(__name__)

# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"

# initialize the app with the extension
db.init_app(app)

import os

app.secret_key = os.environ.get('SECRET_KEY')


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True)
    school = db.Column(db.String, nullable=False)

with app.app_context():
    db.create_all()


@app.post('/add-student')
def add_student():
    name = request.json.get('name')
    email = request.json.get('email')
    school = request.json.get('school')
    new_student = Student(name=name, email=email, school=school)
    db.session.add(new_student)
    db.session.commit()
    return "Student Added Successful!"

@app.get('/students')
def get_students():
    students = Student.query.all()
    students = [{'id':student.id, 'name': student.name, 'email': student.email, 'school': student.school} for student in students]
    return {'students': students}

@app.get('/student/<int:id>')
def get_student(id):
    student = Student.query.filter_by(id=id).first()
    if student:
        student = {'id':student.id, 'name': student.name, 'email': student.email, 'school': student.school}
        return {'student': student}
    return {'message': 'Student not found'}, 404

if __name__ == '__main__':
    app.run(debug=True)