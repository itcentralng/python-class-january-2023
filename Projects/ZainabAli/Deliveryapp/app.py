from flask import Flask, request, sessions
from flask_sqlalchemy import SQLAlchemy
import os
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import generate_password_hash as gph, check_password_hash as cph

db = SQLAlchemy()
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mine.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.secret_key = "hkghafdhgfdhgfjdh"
db.init_app(app)

class User(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     name = db.Column(db.String, nullable=False)
     email = db.Column(db.String, nullable=False)
     phone = db.Column(db.String, nullable=False)
     address = db.Column(db.String, nullable=False)
     payment_info = db.Column(db.String, nullable=False)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String, nullable=False)
    status = db.Column(db.String, nullable=False)
    # products = db.Column(db.String, nullable=False)
    products = db.relationship('Product', backref='order', lazy=True)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)

@app.post('/users')
def create_user():
    name = request.json.get('name')
    email = request.json.get('email')
    phone = request.json.get('phone')
    address = request.json.get('address')
    payment_info = request.json.get('payment_info')
    new_user = User(name=name, email=email, phone=phone, address=address, payment_info=payment_info)
    db.session.add(new_user)
    db.session.commit()
    return "User added successfully"

@app.get('/orders')
def get_orders():
    orders = Order.query.all()
    order = [{'id': Order.id, 'name': Order.name, 'email': Order.email, 'phone': Order.phone, 'address': Order.address, 'payment_info': Order.payment_info} for Order in orders]
    return {'order': order}

@app.post('/orders')
def create_order():
    user_id = request.json.get('user_id')
    products = request.json.get('products')
    order = Order(user_id=user_id, status='pending')
    for product in products:
        product = Product(name=product('name'), price=product('price'), quantity=product('quantity'))
        order.products.append(product)
    db.session.add(order)
    db.session.commit()
    return "Products added successfully."

@app.put('/orders/<int:order_id>')
def update_order_status(order_id):
    order = Order.query.get(order_id)
    if not order:
        return ({'error': 'Order not found'})
    status = request.json('status')
    order.status = statusdb.session.commit()
    return ({'error': 'Order not found'})

if __name__ == '__main__':
    app.run(debug=True) 