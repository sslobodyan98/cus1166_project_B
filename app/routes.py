'''
appointment_date is field in Car table

created web-app email, hardcoded email address and password:

car.maintenance.app1166@gmail.com

password: softwareengineering1166

'''


from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from flask_wtf import form
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, AddVehicle, RegistrationForm, EditVehicleForm, AppNotificationForm
from app.models import User, Car
from datetime import *
import smtplib


@app.route('/')
@app.route('/index')
@login_required
def index():
    cars = [
        {
            'owner': {'user': 'John'},
            'car': 'Testing Car String'
        },
        {
            'owner': {'user': 'Doe'},
            'car': 'Testing Car String2'
        }
    ]
    return render_template('index.html', title='Home', cars=cars)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(user=form.user.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
            return redirect(next_page)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


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
        user = User(user=form.user.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You are now signed up to use our App!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/user/<user>')
@login_required
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
    if form.validate_on_submit():
        car = Car(car_vin=form.car_vin.data, make=form.make.data, model=form.model.data,
                  color=form.color.data, mileage=form.mileage.data)
        db.session.add(car)
        db.session.commit()
        flash('You have added a car to use in our App!')
        return redirect(url_for('login'))
    return render_template('addVehicle.html', title='Add Vehicle', form=form)


@app.route('/editVehicle', methods=['GET', 'POST']) #trying to edit current users
@login_required                                     #vehicle info
def editVehicle():
    form = EditVehicleForm()
    if form.validate_on_submit():
        current_user.car_vin = form.car_vin.data
        current_user.make = form.make.data
        current_user.model = form.model.data
        current_user.color = form.color.data
        current_user.mileage = form.mileage.data
        db.session.commit()
        flash('Your vehicle changes have been saved')
        return redirect(url_for('editVehicle'))
    elif request.method == 'GET':
        form.car_vin.data = current_user.car_vin
        form.make.data = current_user.make
        form.model.data = current_user.model
        form.color.data = current_user.color
        form.mileage.data = current_user.mileage
    return render_template('editVehicle.html', title='Edit Vehicle',
                           form=form)


def getUserEmail(user_id):
    for user in User.users:
        if user.user_id == user_id:
            return user.user_email
    return ' ' #if user email not found return blank string (this should never happen, but required by python)

@app.route('/notificationEmail', methods=['GET', 'POST'])
@login_required
def notificationEmail():
    if request.method == 'GET':
        for car in User.cars:
            delta = car.appointment_date - datetime.datetime.now().date() #appointment_date is field in Car table

            if delta.days==3: #if appointment is in 3 days (only sent on 3rd day before appointment)
                #created gmail for this web application
                #created user_id and passcode, and hardcoded them here:
                gmail_user = 'car.maintenance.app1166@gmail.com'  # sender_email
                gmail_password = 'softwareengineering1166'
                sent_from = gmail_user
                to = getUserEmail(car.user_email)

                # Content to send in email:
                subject = 'User Scheduled Appointment Reminder'
                email_text = "Dear " + User.user + ",\n" + "You have an appointment scheduled in 3 days on " + car.appointment_date + "for your vehicle: \n" + "VIN number: " + car.car_vin + "\n" + "Make: " + car.make + "\n" + "Model: " + car.model + "\n" +"Color: " + car.color + "\n"
                try:
                    server = smtplib.SMTP('smtp.gmail.com', 587)
                    server.ehlo()
                    server.starttls()

                    server.login(gmail_user, gmail_password)
                    server.sendmail(sent_from, to, email_text, subject)
                    server.close()

                    # print('Email sent!')
                except Exception as e:
                    print(e)
                    # print('Something went wrong...')


#APP NOTIFICATION ROUTE: only making connection to html file

@app.route('/appNotification', methods=['GET', 'POST'])
@login_required
def appNotification():
    form = AppNotificationForm()
    return render_template('app_notification.html', title='App Notification', form=form, notification=True)
    return render_template('app_notification.html', title='App Notification', form=form, notification=False)
