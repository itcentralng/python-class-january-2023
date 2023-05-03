from flask import Flask, request, session
from flask_sqlalchemy import SQLAlchemy
import os
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import generate_password_hash as gph, check_password_hash as cph

db = SQLAlchemy()
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mine.db"

app.secret_key = "hsjgsdshagshfghdsakjdhsajhd"
db.init_app(app)

@app.get('/Library')
def welcome():
    return "Welcome to the Library"

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=True)
    author = db.Column(db.String, nullable=False)
    year = db.Column(db.Integer, nullable=True)
    publisher = db.Column(db.String, nullable=False)
    contents = db.Column(db.String, nullable=True)

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True)
    password = db.Column(db.String)

with app.app_context():
    db.create_all()

def authenticate(username, password):
    user = "admin"
    if user==username:
        return user

def identity(playload):
    admin_id = playload['identity']
    return Admin.query.filter_by(id=admin_id).first()

jwt = JWT(app, authenticate, identity)

@app.post('/books')
def create_book():
    name =  request.json.get('name')
    author = request.json.get('author')
    year = request.json.get('year')
    publisher = request.json.get('publisher')
    contents = request.json.get('contents')
    new_book = Book(name=name, author=author, year=year, publisher=publisher, contents=contents)
    db.session.add(new_book)
    db.session.commit() 
    return "Book Added Successfully!"

@app.post('/admin')
def create_admin():
    username = request.json.get('username')
    password = request.json.get('password')
    # password = gph(password)
    new_admin = Admin(username=username, password=password)
    db.session.add(new_admin)
    db.session.commit()
    return "User added successfully"

@app.get('/books')
def get_all_books():
    books = Book.query.all()
    book = [{'id': Book.id, 'name': Book.name, 'author': Book.author, 'year': Book.year, 'publisher': Book.publisher, 'contents': Book.contents}for Book in books]
    return {'book': book}

@app.get('/book/<int:id>')
def get_book(id):
    book = Book.query.filter_by(id=id).first()
    if book:
        book = {'id': book.id, 'name': book.name, 'author': book.author, 'year': book.year, 'publisher': book.publisher, 'contents': book.contents}
        return{'book': book}
    return {'Error': 'Book not found'}

@app.put('/book/<int:index>')
def update_book(index):
    book = Book.query.all()
    name = request.json.get('name')
    author = request.json.get('author')
    year = request.json.get('year')
    publisher = request.json.get('publisher')
    contents = request.json.get('contents')
    if Book:
        Book = [{'id': id, 'name': name, 'author': author, 'year': year, 'publisher': publisher, 'contents': contents}]
        books[index] = books
        return ({'book': book})
    else:
        return ({'Error': 'Book not found'})

@app.delete('/book/<int:index>')
def delete_book(index):
    book = Book.query.all()
    if Book:
        book = [{'id': Book.id, 'name': Book.name, 'author': Book.author, 'year': Book.year, 'publisher': Book.publisher, 'contents': Book.contents}]
        book = books.pop(index)
        return ({'book': book})
    else:
        return ({'Error': 'Book not found'})

@app.post('/login')
def login():
    password = request.json.get('password')
    email = request.json.get('email')
    
if __name__ == '__main__':
    app.run(debug=True)