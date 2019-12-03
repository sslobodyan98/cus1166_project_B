from app import db

class User(db.Model):
    __tablename__= "user"
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    cars = db.relationship('Car', backref='owner', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.user)

class Car(db.Model):
    __tablename__= "car"
    id = db.Column(db.Integer, primary_key=True)
    car_vin = db.Column(db.String(16), index=True, unique=True)
    make = db.Column(db.String(120), index=True)
    model = db.Column(db.String(120), index=True)
    color = db.Column(db.String(64), index=True)
    mileage = db.Column(db.Integer, index=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Car {}'.format(self.car_vin.make.model)
