from flask import Flask, request, session, jsonify
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

timestamp = datetime.now()

db = SQLAlchemy()
app = Flask(__name__)
ma = Marshmallow(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///exchange_wallet.db"
app.config['SECRET_KEY'] = 'swapped_funds'
db.init_app(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    phone = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=timestamp)
    updated_at = db.Column(db.DateTime, nullable=True)


class USDWallet(db.Model):
    __tablename__ = 'usd_wallet'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id'), nullable=False, unique=True)
    dollar_balance = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=timestamp)


class NairaWallet(db.Model):
    __tablename__ = 'naira_wallet'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id'), nullable=False, unique=True)
    naira_balance = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=timestamp)


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User


class USDWalletSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = USDWallet


class NairaWalletSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = NairaWallet


with app.app_context():
    db.create_all()

rate = 450


@app.route("/")
def home():
    return "Exchange running at " + str(timestamp)


@app.post("/register")
def register():
    name = request.json['name']
    email = request.json['email']
    phone = request.json['phone']
    password = request.json['password']

    check_phone = User.query.filter_by(phone=phone).first()
    check_email = User.query.filter_by(email=email).first()
    if check_phone or check_email:
        return {"message": "Phone number or email already exists"}, 400

    new_user = User(name=name, email=email, phone=phone, password=password)
    db.session.add(new_user)
    db.session.commit()
    return {"message": "User created successfully"}


@app.post("/swap")
def swap():
    user_id = request.json['user_id']
    to_currency = request.json['to_currency']
    amount = request.json['amount']

    if user_id and to_currency and amount:
        swap(user_id, to_currency, amount)
    else:
        return {"message": "Please provide user_id, to_currency, amount"}, 400


def swap(user_id, to_currency, amount):
    usd_wallet = USDWallet.query.filter_by(user_id=user_id).first()
    naira_wallet = NairaWallet.query.filter_by(user_id=user_id).first()

    if to_currency == "NGN":
        if usd_wallet.dollar_balance < amount:
            return {"message": "Insufficient USD funds"}, 400

        usd_wallet.dollar_balance -= amount  # deduct exact dollar amount
        # convert dollar amount to naira and topup to wallet
        naira_wallet.naira_balance += (amount * rate)
        db.session.commit()
        return {"message": "Swap of {} USD to NGN successful".format(amount)}

    elif to_currency == "USD":
        if naira_wallet.naira_balance < amount:
            return {"message": "Insufficient NGN funds"}, 400

        naira_wallet.naira_balance -= amount  # deduct exact naira amount
        # convert naira amount to dollar and topup to wallet
        usd_wallet.dollar_balance += (amount / rate)
        db.session.commit()
        return {"message": "Swap of {} NGN to USD successful".format(amount)}
    else:
        return {"message": "Invalid currency, please use USD or NGN"}, 400
