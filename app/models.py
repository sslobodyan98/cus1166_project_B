from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String, index=True)
    cars = db.relationship('Car', backref='owner', lazy='dynamic')

    def __init__(self, user, email, role):
        self.user = user
        self.email = email
        self.role = role

    def __repr__(self):
        return '<User {}>'.format(self.user)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_role(self, role):
        return role


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(16), index=True)
    car_vin = db.Column(db.String(16), index=True, unique=True)
    make = db.Column(db.String(120), index=True)
    model = db.Column(db.String(120), index=True)
    color = db.Column(db.String(64), index=True)
    mileage = db.Column(db.Integer, index=True)
    miles_until_oil_change = db.Column(db.Integer, index=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))



    def __init__(self, user,car_vin, make, model, color, mileage):
        self.user = user
        self.car_vin = car_vin
        self.make = make
        self.model = model
        self.color = color
        self.mileage = mileage

    def __repr__(self):
        return '<Car {}'.format(self.user.car_vin.make.model.color.mileage)
        return '<Car VIN {}, Car Make{}>'.format(self.car_vin, self.make)

    def return_car_vin(self):
        return '<Car Make {}>'.format(self.make)


class Availability(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(20), index=True)
    date = db.Column(db.Date, index=True)
    start_time = db.Column(db.Time, index=True)
    end_time = db.Column(db.Time, index=True)

    def __repr__(self):
        return '<Availability {}'.format(self.user.date.start_time.end_time)


class Schedules(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(20), index=True)
    vehicle = db.Column(db.String, index=True)
    mechanic = db.Column(db.String, index=True)
    appointment_date = db.Column(db.Date, index=True)
    appointment_time = db.Column(db.Time, index=True)

    def __repr__(self):
        return '<Schedules {}'.format(self.user.mechanic.appointment_date.appointment_time)
