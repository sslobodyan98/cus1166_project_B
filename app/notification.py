from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import Car
from flask import Flask, app
from flask_mail import Mail, Message
import smtplib

app.config['DEBUG'] = True
app.config['TESTING'] = False
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
# app.config['MAIL_DEBUG'] = True
app.config['MAIL_USERNAME'] = 'mariyamelshrieff@gmail.com'
app.config['MAIL_PASSWORD'] = 'AD22703259me'
app.config['MAIL_DEFAULT_SENDER'] = 'mariyamelshrieff@gmail.com'
app.config['MAIL_MAX_EMAILS'] = None
# app.config['MAIL_SUPPRESS_SEND'] = False
app.config['MAIL_ASCII_ATTATCHMENTS'] = False

mail = Mail(app)


def check_and_notify(Car):
    difference = Car.update_miles - Car.mileage

    if difference > 5000:
        miles_until_next_oil_change = difference
        return miles_until_next_oil_change, False

    elif difference <= 5000:
        miles_until_next_oil_change = 0

        msg = Message('Oil Change Reminder Notification', recipients=['car.maintenance.app1166@gmail.com'])
        msg.body = 'Hi, Its time for you to schedule your next car maintenance appointment as your oil needs to be ' \
                   'changed! '
        msg.html = '<b>This is a Reminder Notification </b>'

        mail.send(msg)
        return miles_until_next_oil_change, True,

    # adding update_miles to mileage AFTER USER DOES OIL CHANGE:
    mileage = Car.mileage + Car.update_miles
    return mileage
