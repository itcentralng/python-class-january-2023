from datetime import datetime
from flask import Flask, request, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate

date = datetime.now()

db = SQLAlchemy()
app = Flask(__name__)
migrate = Migrate(app, db)
ma = Marshmallow(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///quizgenius_db.db"
app.config['SECRET_KEY'] = 'have_fun_with_quizgenius'

db.init_app(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=True)


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User


class Question(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String, nullable=False)
    options = db.Column(db.String, nullable=False)
    answer = db.Column(db.String, nullable=False)
    time_limit = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=True)


class QuestionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Question


class Score(db.Model):
    __tablename__ = 'scores'
    id = db.Column(db.Integer, primary_key=True)
    # quiz_id = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=True)


class ScoreSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Score


with app.app_context():
    db.create_all()

# user_schema = UserSchema()
# question_schema = QuestionSchema()
# score_schema = ScoreSchema()


@app.route("/")
def hello_world():
    return "QuizGenius running at " + str(date)

# Setters


@app.post("/create/user")
def user():
    name = request.json.get('name')
    email = request.json.get('email')
    username = request.json.get('username')
    password = request.json.get('password')

    user = User.query.filter_by(email=email).first()
    if user:
        return "Email already exists", 409

    user = User.query.filter_by(username=username).first()
    if user:
        return "Username already exists", 409

    new_user = User(name=name, email=email, username=username,
                    password=password, created_at=date)
    db.session.add(new_user)
    db.session.commit()
    return "User saved successfully"


@app.post("/create/question")
def question():
    question = request.json.get('question')
    options = request.json.get('options')
    answer = request.json.get('answer')
    time_limit = request.json.get('time_limit')
    new_question = Question(question=question, options=options, answer=answer, time_limit=time_limit,
                            created_at=date)
    db.session.add(new_question)
    db.session.commit()
    return "Question saved successfully"


@app.post("/create/score")
def score():
    user_id = request.json.get('user_id')
    score = request.json.get('score')
    new_score = Score(user_id=user_id, score=score, created_at=date)
    db.session.add(new_score)
    db.session.commit()
    return "Score saved successfully"

# All Getters


@app.get("/list/users")
def list_users():
    users = User.query.all()
    users = [{"id": user.id, "name": user.name, "email": user.email, "username": user.username,
              "password": user.password, "created_at": user.created_at, "updated_at": user.updated_at} for user in users]
    return {"users": users}


@app.get("/list/questions")
def list_questions():
    questions = Question.query.all()
    questions = [{"id": question.id, "question": question.question, "options": question.options,
                  "created_at": question.created_at, "updated_at": question.updated_at} for question in questions]
    return {"questions": questions}


@app.get("/list/scores")
def list_scores():
    scores = Score.query.all()
    scores = [{"id": score.id, "user_id": score.user_id, "score": score.score,
               "created_at": score.created_at, "updated_at": score.updated_at} for score in scores]
    return {"scores": scores}

# Single End-Point Getter


@app.get('/user/<int:id>')
def get_user(id):
    user = User.query.filter_by(id=id).first()
    if user:
        user = {"id": user.id, "name": user.name, "email": user.email, "username": user.username,
                "password": user.password, "created_at": user.created_at, "updated_at": user.updated_at}
        return {"user": user}, 200
    return "User not found", 404


@app.get('/question/<int:id>')
def get_question(id):
    question = Question.query.filter_by(id=id).first()
    if question:
        question = {"id": question.id, "question": question.question, "options": question.options,
                    "answer": question.answer, "created_at": question.created_at, "updated_at": question.updated_at}
        return {"question": question}, 200
    return "Question not found", 404


@app.get('/score/<int:user_id>')
def get_user_score(user_id):
    score = Score.query.filter_by(user_id=user_id).all()
    if score:
        score = [{"id": score.id, "score": score.score, "created_at": score.created_at,
                  "updated_at": score.updated_at} for score in score]
        return {"score": score}, 200
    return "Score not found", 404


@app.get("/leaderboard")
def leaderboard():
    scores = Score.query.all()
    scores_list = [{"id": score.id, "user_id": score.user_id,
                    "score": score.score} for score in scores]
    return {"leaderboard": scores_list}


if __name__ == "__main__":
    app.run()
