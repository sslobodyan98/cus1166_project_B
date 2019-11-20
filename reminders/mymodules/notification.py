from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import Car


def check_and_notify (Car):

    difference = Car.update_miles - Car.mileage

    if difference > 5000:
        miles_until_next_oil_change = difference
        return miles_until_next_oil_change, False

    elif difference <= 5000:
        miles_until_next_oil_change = 0
        return miles_until_next_oil_change, True

    #adding update_miles to mileage AFTER USER DOES OIL CHANGE:
    mileage = Car.mileage + Car.update_miles
    return mileage
