from flask import Flask, request, session
from flask_sqlalchemy import SQLAlchemy
import os
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import generate_password_hash as gph, check_password_hash as cph

db = SQLAlchemy()

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"

app.secret_key = "jshldafergfhbfjdksd"

db.init_app(app)

@app.get('/')
def welcome():
    return "Welcome to my Hospital"

class Hospital(db.Model):
    name = db.Column(db.String, nullable=True)
    administration = db.Column(db.String, nullable=True)
    services = db.Column(db.String, nullable=False)
    schools = db.Column(db.String, nullable=True)
    departments = db.Column(db.String, nullable=False)
    news = db.Column(db.String, nullable=True)

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True)
    password = db.Column(db.String)

with app.app_context():
    db.create_all()

def authenticate(username, password):
    user = "admin"
    if username==username:
        return user

def identity(playload):
    admin_id = playload['identity']
    return Admin.query.filter_by(id=admin_id).first()

jwt = JWT(app, authenticate, identity)

@app.post('/hospital')
def create_all():
    name = request.json.get('name')
    services = request.json.get('services')
    administration = request.json.get('administration')
    schools = request.json.get('schools')
    departments = request.json.get('departments')
    news = request.json.get('news')
    new_hospital = Hospital(name=name, services=services, administration=administration, schools=schools, departments=departments, news=news)
    db.session.add(new_hospital)
    db.session.commit()
    return "Hospital added successfully."

@app.get('/hospital')
def get_all():
    hospital = Hospital.query.all()
    book = [{'name': hospital.name, 'services': hospital.services, 'administration': hospital.administration, 'schools': hospital.schools, 'department': hospital.department, 'news': hospital.news} for hospital in Hospital]
    return {'hospital': hospital}

@app.put('/update_hospital')
def update_hospital():
    Hospital = Hospital.query.all()
    name = request.json.get('name')
    services = request.json.get('services')
    administration = request.json.get('administration')
    schools = request.json.get('schools')
    departments = request.json.get('departments')
    news = request.json.get('news')

    hospital.name = name or hospital.name
    hosptial.services = services or hospital.services
    hospital.administration = administration or hospital.administration
    hospital.schools = schools or hospital.schools
    hospital.departments = departments or hospital.departments
    hospital.news = news or hospital.news

    db.session.commit()
    return "Hospital updated successfully!"

@app.post('/login')
def login():
    username = request.json.get('username')
    password = request.json.get('password')

if __name__ == '__main__':
    app.run(debug=True)
