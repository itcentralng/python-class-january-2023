from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import generate_password_hash as gph, check_password_hash as cph

db = SQLAlchemy()
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mine.db"

app.secret_key = "lkdhafgsdfgdshfggsdf"
db.init_app(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True)
    password = db.Column(db.String, nullable=False)

    def init(self, username, password):
        self.username = username
        self.password = password
    
    def repr(self):
        return '<User %r>' % self.username

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String)
    answer = db.Column(db.String)
    points = db.Column(db.Integer)

    def init(self, question, answer, points):
        self.question = question
        self.answer = answer
        self.points = points

    def repr(self):
        return '<Quiz %r>' % self.question

def authenticate(username, password):
    user = User.query.filter_by(username=username).first()
    if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
        return user

def identity(payload):
    user_id = payload['identity']
    return User.query.get(user_id)

jwt = JWT(app, authenticate, identity)

questions = [
    {
        'question': 'who is the President of Nigeria?',
        'answer': 'Gen. Muhammadu Buhari',
        'points': 1
    },
    {
        'question': 'How many states and capitals do we have in Nigeria?',
        'answer': 'We have 36 states and capitals in Nigeria',
        'points': 1
    },
    {
        'question': 'Who is the current Governor of Kaduna state?',
        'answer': 'Mal. Nasiru Ahmad Elrufai',
        'points': 1
    },
    {
        'question': 'What is the capital of Kaduna state?',
        'answer': 'Kaduna',
        'points': 1

    },
    {
        'question': 'Zaria local government is under what state?',
        'answer': 'Kaduna staete',
        'points': 1
    },
    {
        'question': 'Which state has the largest populations in Nigeria?',
        'answer': 'Kano state',
        'points': 1
    }
]

@app.post('/questions')
def create_questions():
    for question in questions:
        db.session.add(Quiz(**question))
    db.session.commit()

@app.get('/questions')
def get_questions():
    return Quiz.query.all()

@app.get('/questions/<init:answers>')
def calculate_score(answers):
    score = 0
    for answer in answers:
        question = Quiz.query.filter_by(id=answer['id']).first()
        if question and question.answer.lower() == answer['answer'].lower():
            score += question.points
        return score

@app.route('/quiz')
def get_quiz():
    questions = get_questions()
    return jsonify ([{'id': q.id,
                      'question': q.question,
                      'points': q.points} for q in questions])

if __name__ == '__main__':
    app.run(debug=True)