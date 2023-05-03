from flask import Flask, request, session, jsonify
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

timestamp = datetime.now()

db = SQLAlchemy()
app = Flask(__name__)
ma = Marshmallow(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///our_visitors.db"
app.config['SECRET_KEY'] = 'track_visitors'
db.init_app(app)


class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    phone = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=timestamp)
    updated_at = db.Column(db.DateTime, nullable=True)


class Staff(db.Model):
    __tablename__ = 'staff'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    avaibility = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=timestamp)
    updated_at = db.Column(db.DateTime, nullable=True)


class Visitor(db.Model):
    __tablename__ = 'visitors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    address = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=timestamp)
    updated_at = db.Column(db.DateTime, nullable=True)


class VisitingLog(db.Model):
    __tablename__ = 'visiting_log'
    id = db.Column(db.Integer, primary_key=True)
    submitted_by = db.Column(db.Integer, db.ForeignKey('admin.id'))
    admin = db.relationship("Admin")
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.id'))
    staff = db.relationship("Staff")
    visitor_id = db.Column(db.Integer, db.ForeignKey('visitors.id'))
    visitor = db.relationship("Visitor")
    reason_for_visit = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=timestamp)
    left_at = db.Column(db.DateTime, nullable=True)


class AdminSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Admin


class StaffSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Staff


class VisitorSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Visitor


class VisitingLogSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = VisitingLog
        include_relationships = True
        include_fk = True
    admin = ma.Nested(AdminSchema)
    staff = ma.Nested(StaffSchema)
    visitor = ma.Nested(VisitorSchema)


class ActiveVisitorsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = VisitingLog
        include_relationships = True
        include_fk = True
    staff = ma.Nested(StaffSchema)
    visitor = ma.Nested(VisitorSchema)


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return "Visitors App running at " + str(timestamp)


@app.post("/register/admin")
def register_admin():
    new_admin = Admin(
        name=request.json['name'],
        email=request.json['email'],
        phone=request.json['phone'],
        password=request.json['password']
    )

    admin_exist = Admin.query.filter_by(
        phone=new_admin.phone, email=new_admin.email).first()
    if admin_exist:
        return {"message": "Phone number or email already exists"}, 400

    db.session.add(new_admin)
    db.session.commit()
    return {"message": "Admin account created successfully"}, 200


@app.post("/register/staff")
def register_staff():
    new_staff = Staff(
        name=request.json['name'],
        role=request.json['role'],
        email=request.json['email'],
        phone=request.json['phone']
    )
    staff_exist = Staff.query.filter_by(
        phone=new_staff.phone, email=new_staff.email).first()
    if staff_exist:
        return {"message": "Phone number or email already exists"}, 400
    db.session.add(new_staff)
    db.session.commit()
    return {"message": "Staff account created successfully"}, 200


@app.post('/register/visitor')
def register_visitor():
    new_visitor = Visitor(
        name=request.json['name'],
        phone=request.json['phone'],
        email=request.json['email'],
        address=request.json['address']
    )
    visitor_exist = Visitor.query.filter_by(
        phone=new_visitor.phone, email=new_visitor.email).first()

    # create and return visitor if not exist
    if not visitor_exist:
        db.session.add(new_visitor)
        db.session.commit()
        return {
            "message": "new visitor",
            "profile": VisitorSchema().dump(new_visitor)
        }, 200

    return {
        "message": "existing visitor",
        "profile": VisitorSchema().dump(visitor_exist)
    }, 200


@app.post("/log")
def log_visit():
    new_log = VisitingLog(
        submitted_by=request.json['submitted_by'],
        staff_id=request.json['staff_id'],
        visitor_id=request.json['visitor_id'],
        reason_for_visit=request.json['reason_for_visit']
    )

    admin = Admin.query.filter_by(id=new_log.submitted_by).first()
    visitor = Visitor.query.filter_by(id=new_log.visitor_id).first()
    staff = Staff.query.filter_by(id=new_log.staff_id).first()

    if not admin:
        return {"message": "Admin profile not found"}, 404

    if not staff:
        return {"message": "Staff profile not found"}, 404

    if staff.avaibility is False:
        return {"message": "Staff not available"}, 404

    if not visitor:
        return {"message": "Visitor profile not found"}, 404

    db.session.add(new_log)
    db.session.commit()
    return {"message": "Logged successfully, be sure to logout when visitor leaves"}, 200


@app.patch("/logout")
def logout_visit():
    log_id = request.json['log_id']
    log = VisitingLog.query.filter_by(id=log_id).first()
    if log:
        log.left_at = timestamp
        db.session.commit()
        return {"message": "Visitor logged out successfully"}, 200

    return {"message": "Invalid log id"}, 404


@app.patch("/staff/availability")
def staff_availability():
    staff_id = request.json['staff_id']
    staff = Staff.query.filter_by(id=staff_id).first()
    if staff:
        staff.avaibility = not staff.avaibility
        db.session.commit()
        return {"message": "Staff availability updated successfully"}, 200

    return {"message": "Invalid staff id"}, 404


@app.get("/list/admin")
def get_admins():
    admins = Admin.query.all()
    admins_list = AdminSchema().dump(admins, many=True)
    return {"admins": admins_list}


@app.get("/list/staff")
def get_staff():
    staff = Staff.query.all()
    staff_list = StaffSchema().dump(staff, many=True)
    return {"staff": staff_list}


@app.get("/list/visitor")
def get_visitors():
    visitors = Visitor.query.all()
    visitors_list = VisitorSchema().dump(visitors, many=True)
    return {"visitors": visitors_list}


@app.get("/list/logs")
def get_visitors_log():
    visiting_log = VisitingLog.query.all()
    visiting_log_list = VisitingLogSchema().dump(visiting_log, many=True)
    return {"visiting_log": visiting_log_list}


@app.get("/list/active_logs")
def get_active_visitors_log():
    visiting_log = VisitingLog.query.filter_by(left_at=None).all()
    visiting_log_list = ActiveVisitorsSchema().dump(visiting_log, many=True)
    return {"visiting_log": visiting_log_list}


@app.get("/view/admin/<int:admin_id>")
def get_an_admin(admin_id):
    admin = Admin.query.filter_by(id=admin_id).first()
    if admin:
        admin_profile = AdminSchema().dump(admin)
        return {"admin": admin_profile}

    return {"message": "Admin profile not found"}, 404


@app.get("/view/staff/<int:staff_id>")
def get_a_staff(staff_id):
    staff = Staff.query.filter_by(id=staff_id).first()
    if staff:
        staff_profile = StaffSchema().dump(staff)
        return {"staff": staff_profile}

    return {"message": "Staff profile not found"}, 404


@app.get("/view/visitor/<int:visitor_id>")
def get_a_visitor(visitor_id):
    visitor = Visitor.query.filter_by(id=visitor_id).first()
    if visitor:
        visitor_profile = VisitorSchema().dump(visitor)
        return {"visitor": visitor_profile}

    return {"message": "Visitor profile not found"}, 404


@app.get("/view/logs/<int:log_id>")
def get_visiting_log(log_id):
    log = VisitingLog.query.filter_by(id=log_id).first()
    if log:
        visit_log = VisitingLogSchema().dump(log)
        return {"log": visit_log}

    return {"message": "Log record not found"}, 404
