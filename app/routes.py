from datetime import datetime, timedelta, date
import calendar
from flask import Flask
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from flask_mail import Mail, Message
from app import app, db
from app.forms import *
from app.models import *
from app.models import User, Car, Availability, Schedules
import string
import random

app.config['DEBUG'] = True
app.config['TESTING'] = False
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
# app.config['MAIL_DEBUG'] = True
app.config['MAIL_USERNAME'] = 'groupbsoftwareengineering1166@gmail.com'
app.config['MAIL_PASSWORD'] = 'SoftwareEngineering1166'
app.config['MAIL_DEFAULT_SENDER'] = 'groupbsoftwareengineering1166@gmail.com'
app.config['MAIL_MAX_EMAILS'] = None
# app.config['MAIL_SUPPRESS_SEND'] = False  # comment out in production!
app.config['MAIL_ASCII_ATTACHMENTS'] = False

mail = Mail(app)


# def appointment_reminder():
#     appointments = Schedules.query.all()
#     users = User.query.all()
#
#     with app.app_context():
#         for x in appointments:
#             diff = x.appointment_date - datetime.date.today()
#             for i in users:
#                 if diff.days == 3 and i.user == x.user and i.role == 'Car Owner':
#                     msg = Message('Appointment Reminder Notification', recipients=[i.email])
#                     msg.html = 'Hello, You have an appointment scheduled in 3 days. We hope to see you!'
#                     mail.send(msg)
#                 if diff.days < 1 and i.user == x.user and i.role == 'Car Owner':
#                     msg = Message('Follow up for oil change appointment', recipients=[i.email])
#                     msg.body = 'Hello, I hope your appointment went well. If you could please take the brief survey ' \
#                                'and review your mechanic we would highly appreciate it.'
#                     msg.html = 'Hello, I hope your appointment went well. If you could please take the brief survey ' \
#                                'and review your mechanic we would highly appreciate it.' \
#                                ' <a href="http://127.0.0.1:5000/review_appointment"> Click here to access review</a>'
#                     mail.send(msg)
#                 if diff.days < 1 and x.mechanic == i.user and i.role == 'Mechanic':
#                     msg = Message('Follow up for oil change appointment', recipients=[i.email])
#                     msg.body = 'Hello, I hope your appointment went well. If you could please take the brief survey ' \
#                                'and review your mechanic we would highly appreciate it.'
#                     msg.html = 'Hello, I hope your appointment went well. If you could please take a second to ' \
#                                'suggest other repairs that the customer may need we would highly appreciate it.' \
#                                '<a href="http://127.0.0.1:5000/suggest_recommendations"> Click here to access ' \
#                                'review</a> '
#                     mail.send(msg)
#
#     return app
#
#
# appointment_reminder()


@app.route('/')
@app.route('/index')
@login_required
def index():
    cars = Car.query.all()
    appointments = Schedules.query.all()
    return render_template('index.html', title='Home', cars=cars, appointments=appointments)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():

        user = User.query.filter_by(user=form.user.data).first()

        if user.role == 'Car Owner' and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('index'))
        elif user.role == 'Mechanic' and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('mechanicDashboard'))
    return render_template('login.html', title='Sign In', form=form)


def GenerateRandomPassword():
    string.ascii_letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    temp_password = ''
    for i in [1, 2, 3, 4]:
        temp_password += random.choice(string.ascii_letters)
    return temp_password


@app.route('/forgotPassword', methods=['GET', 'POST'])
def ForgotPassword():
    form = ForgotPasswordForm()
    users = User.query.all()  # query through users
    if form.validate_on_submit():  # if submit button is pressed
        for x in users:  # for users
            if x.user == form.user.data:  # if a user in users == username entered in form
                # set temp_password:
                temp_password = GenerateRandomPassword()
                x.set_password(temp_password)
                db.session.commit()
                # send email:
                msg = Message('Forgot Password', recipients=[x.email])
                msg.body = ' '
                msg.html = 'Here is your temporary password: ' + temp_password + '<a' \
                                                                                 'Use this password to sign into your account.</a>'
                mail.send(msg)
    return render_template('forgot_password.html', title='Forgot Password', form=form)


@app.route('/resetPassword', methods=['GET', 'POST'])
def ResetPassword():
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(user=current_user.user).first()  # get user
        user.set_password(form.password.data)  # set new password data that they entered
        db.session.commit()
        flash('Your password has been changed')
        return redirect(url_for('login'))  # redirect to login page
    return render_template('reset_password.html', title='Reset Password', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(user=form.user.data, email=form.email.data, role=form.role.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You are now signed up to use our App!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/user/<user>')
def user(user):
    user = User.query.filter_by(user=user).first_or_404()
    cars = [
        {'owner': user, 'car_vin': 'Test post #1'},
        {'owner': user, 'car_vin': 'Test post #2'}
    ]
    return render_template('user.html', user=user, cars=cars)


@app.route('/addVehicle', methods=['GET', 'POST'])
def RegisterCar():
    form = AddVehicle()
    cars = Car.query.all()
    if form.validate_on_submit():
        car = Car(user=current_user.user, car_vin=form.car_vin.data, make=form.make.data, model=form.model.data,
                  color=form.color.data, mileage=form.mileage.data, registration_date=form.registration_date.data)
        for x in cars:
            old = x.registration_date
            x.registration_date = old + timedelta(days=365)

        db.session.add(car)
        db.session.commit()
        # Assuming every time a user adds a car to their fleet, their previous vehicle inspections will be pushed back 1 year

        flash('You have added a car to use in our App!')
        return redirect(url_for('index'))
    return render_template('addVehicle.html', title='Add Vehicle', form=form, cars=cars)


