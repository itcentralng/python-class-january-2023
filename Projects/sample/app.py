from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message

app = Flask(__name__)

app.secret_key = 'secret_key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'naseer.mustapher@gmail.com'
app.config['MAIL_PASSWORD'] = 'vwdtsvqjqobqkupc'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

db = SQLAlchemy(app)
mail = Mail(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)

with app.app_context():
    db.create_all()

@app.get('/')
def index():
    return 'Welcome to Flask App'

@app.post('/register')
def register():
    email = request.json['email']
    password = request.json['password']
    name = request.json['name']
    user = User(email=email, password=password, name=name)
    db.session.add(user)
    db.session.commit()
    msg = Message(
        'Welcome to Flask App', 
        sender="naseer.mustapher@gmail.com",
        recipients=[email]
    )
    msg.body = f"Hi {name}, Welcome to Flask App"
    msg.html = render_template('welcome.html', name=name)
    mail.send(msg)
    return 'User Registered Successfully'