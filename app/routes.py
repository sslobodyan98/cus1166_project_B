from datetime import datetime, timedelta, date
import calendar
from flask import Flask
from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from flask_mail import Mail, Message
from sqlalchemy import func
#import paypalrestsdk

from app import app, db
from app.forms import *
from app.models import *
from app.models import User, Car, Availability, Schedules
import string
import random

app.config['DEBUG'] = True
app.config['TESTING'] = False

# paypalrestsdk.configure({
#     "mode": "sandbox",  # sandbox or live
#     "client_id": "AZjCcKtxPjinLV1ZX_e_jJ7qPAfV9MTCOwdn2-Ehsv4hrsRWndTrHcIrKBH5CExCJ2OrmLr30v995MdK",
#     "client_secret": "EOpjc-2uD385GWOOmiWc863OajXPOwp-wbdPFg3fK72_F0sxv5T7-QXMY1evWfD_HQ6NXWwJVo5MyEnV"})


# app.config['MAIL_SERVER'] = 'smtp.gmail.com'
# app.config['MAIL_PORT'] = 587
# app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USE_SSL'] = False
# # app.config['MAIL_DEBUG'] = True
# app.config['MAIL_USERNAME'] = 'groupbsoftwareengineering1166@gmail.com'
# app.config['MAIL_PASSWORD'] = 'SoftwareEngineering1166'
# app.config['MAIL_DEFAULT_SENDER'] = 'groupbsoftwareengineering1166@gmail.com'
# app.config['MAIL_MAX_EMAILS'] = None
# # app.config['MAIL_SUPPRESS_SEND'] = False  # comment out in production!
# app.config['MAIL_ASCII_ATTACHMENTS'] = False
#
# mail = Mail(app)
#
#
# def appointment_reminder():
#     appointments = Schedules.query.all()
#     users = User.query.all()
#     today = date.today()
#     with app.app_context():
#         for x in appointments:
#             diff = x.appointment_date - today
#             for i in users:
#                 if diff.days == 3 and i.user == x.user :
#                     msg = Message('Appointment Reminder Notification', recipients=[i.email])
#                     msg.html = 'Hello, You have an appointment scheduled in 3 days. We hope to see you!'
#                     mail.send(msg)
#                 if diff.days < 1 and i.user == x.user :
#                     msg = Message('Follow up for oil change appointment', recipients=[i.email])
#                     msg.body = 'Hello, I hope your appointment went well. If you could please take the brief survey ' \
#                                'and review your mechanic we would highly appreciate it.'
#                     msg.html = 'Hello, I hope your appointment went well. If you could please take the brief survey ' \
#                                'and review your mechanic we would highly appreciate it.' \
#                                ' <a href="http://127.0.0.1:5000/review_appointment"> Click here to access review</a>'
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


@app.route('/DeleteCar/<int:id>', methods=['GET', 'POST'])
def deleteCar(id):
    Car.query.filter_by(id=id).delete()
    db.session.commit()

    return redirect(url_for('index'))


@app.route('/addAvailability', methods=['GET', 'POST'])
def addAvailability():
    form = AddAvailability()
    if form.validate_on_submit():
        time = Availability(user=current_user.user, date=form.date.data, start_time=form.start_time.data,
                            end_time=form.end_time.data)
        db.session.add(time)
        db.session.commit()
        return redirect(url_for('mechanicDashboard'))
    return render_template('Mechanic_AvaialablityForm.html', title='Add availability', form=form)


@app.route('/ScheduleAppointment', methods=['GET', 'POST'])
def Schedule():
    form = ScheduleAppointment()
    availabilities = Availability.query.all()
    mechanics = User.query.filter_by(role="Mechanic")
    if form.validate_on_submit():
        appointments = Schedules.query.all()
        for x in appointments:

            if x.appointment_date == form.date.data and x.appointment_time == form.start_time.data and \
                    x.mechanic == form.mechanic.data:
                return redirect(url_for('Schedule'))
                flash("try again")
        for i in availabilities:
            if i.user == form.mechanic.data and i.date == form.date.data and (form.start_time.data < i.start_time or
                                                                              form.start_time.data > i.end_time):
                return redirect(url_for('Schedule'))
                flash("try again")
        for i in availabilities:
            if i.user == form.mechanic.data and i.date == form.date.data and (
                    form.start_time.data < i.start_time or form.start_time.data > i.end_time):
                return redirect(url_for('Schedule'))
                flash("try again")
        meeting = Schedules(user=current_user.user, mechanic=form.mechanic.data, appointment_date=form.date.data,
                            appointment_time=form.start_time.data, vehicle=form.vehicle.data,
                            appointment_type=form.appointment_type.data, status='PENDING')
        db.session.add(meeting)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('ScheduleAppointment.html', title='Schedule Appointment', form=form, mechanics=mechanics)


@app.route('/EditAppointment/<int:id>', methods=['GET', 'POST'])
def editAppointment(id):
    form = ScheduleAppointment()
    print(form.validate_on_submit())
    error = None
    if form.validate_on_submit():
        appointments = Schedules.query.all()
        availabilities = Availability.query.all()
        for x in appointments:
            if x.appointment_date == form.date.data and x.appointment_time == form.start_time.data and \
                    x.mechanic == form.mechanic.data and x.id != id:
                return redirect(url_for('editAppointment', id=id))
        for i in availabilities:
            if i.user == form.mechanic.data and i.date == form.date.data and (form.start_time.data < i.start_time or
                                                                              form.start_time.data > i.end_time):
                return redirect(url_for('Schedule'))

        current_appointment = Schedules.query.filter_by(id=id).first_or_404()
        current_appointment.vehicle = form.vehicle.data
        current_appointment.mechanic = form.mechanic.data
        current_appointment.appointment_date = form.date.data
        current_appointment.appointment_time = form.start_time.data
        current_appointment.appointment_type = form.appointment_type.data

        db.session.add(current_appointment)
        db.session.commit()

        return redirect(url_for('index'))

    current_appointment = Schedules.query.filter_by(id=id).first_or_404()

    form.vehicle.data = current_appointment.vehicle
    form.mechanic.data = current_appointment.mechanic
    form.date.data = current_appointment.appointment_date
    form.start_time.data = current_appointment.appointment_time
    form.appointment_type.data = current_appointment.appointment_type
    return render_template('ScheduleAppointment.html', title='Edit Appointment', form=form, error=error)


@app.route('/DeleteAppointment/<int:id>', methods=['GET', 'POST'])
def deleteAppointment(id):
    Schedules.query.filter_by(id=id).delete()
    db.session.commit()

    return redirect(url_for('index'))


@app.route('/Confirmed/<int:id>', methods=['GET', 'POST'])
@login_required
def Confirmed(id):
    current_appointment = Schedules.query.filter_by(id=id).first_or_404()
    current_appointment.status = 'CONFIRMED'
    db.session.commit()
    return redirect(url_for('mechanicDashboard'))


@app.route('/Declined/<int:id>', methods=['GET', 'POST'])
@login_required
def Declined(id):
    current_appointment = Schedules.query.filter_by(id=id).first_or_404()
    current_appointment.status = 'DECLINED'
    db.session.commit()
    return redirect(url_for('mechanicDashboard'))


# @app.route('/Paid/<int:id>', methods=['GET', 'POST'])
# @login_required
# def Paid(id):
#     current_appointment = Schedules.query.filter_by(id=id).first_or_404()
#     current_appointment.status = 'Paid'
#     db.session.commit()
#     return redirect(url_for('mechanicDashboard'))
#
# @app.route('/NotPaid/<int:id>', methods=['GET', 'POST'])
# @login_required
# def NotPaid(id):
#     current_appointment = Schedules.query.filter_by(id=id).first_or_404()
#     current_appointment.status = 'Not Paid'
#     db.session.commit()
#     return redirect(url_for('mechanicDashboard'))


@app.route('/DisplayAvailability', methods=['GET', 'POST'])
def DisplayAvailabilities():
    availabilities = Availability.query.all()
    appointments = Schedules.query.all()
    return render_template('DisplayMechanicAvailability.html',
                           availabilities=availabilities, appointments=appointments)


@app.route('/oil_change', methods=['GET', 'POST'])
@login_required
def OilChange():
    form = OilChangeForm()
    cars = Car.query.all()
    if form.validate_on_submit():  # if submit button is pressed
        for x in cars:
            if x.user == current_user.user and x.model == form.car.data:
                difference = form.update_miles.data - x.mileage
                x.miles_until_oil_change = 5000 - difference
                x.mileage = form.update_miles.data
                db.session.commit()
        if difference < 5000:
            return redirect(url_for('index'))
        elif difference >= 5000:
            msg = Message('Oil Change Reminder Notification', recipients=[current_user.email])
            msg.body = 'Hi, Its time for you to schedule your next car maintenance appointment as your oil needs to ' \
                       'be changed! '
            msg.html = '<b>This is a Reminder Notification </b>'
            mail.send(msg)
            return redirect(url_for('Schedule'))

    return render_template('oil_change.html', title='Oil Change', form=form, cars=cars)


@app.route('/mechanicDashboard', methods=['GET', 'POST'])
@login_required
def mechanicDashboard():
    appointments = Schedules.query.order_by(func.DATE(Schedules.appointment_date)).all()
    form = ConfirmAppointmentCompletedForm()
    form2 = ConfirmAppointmentPaidForm()

    return render_template('mechanicDashboard.html', title='Mechanic Dashboard', appointments=appointments, form=form,
                           form2=form2)


@app.route('/review_appointment', methods=['GET', 'POST'])
@login_required
def rate_mechanic():
    form = ReviewMechanic()
    all_reviews = Reviews.query.order_by(Reviews.mechanic)
    all_averages = Mechanic_Ratings.query.all()
    if form.validate_on_submit():
        total = 0
        total_reviews = []
        review_made = Reviews(mechanic=form.mechanic.data, comment=form.comments.data, rating=form.rating.data,
                              user=current_user.user)
        db.session.add(review_made)

        for x in all_reviews:
            if x.mechanic == form.mechanic.data:
                total_reviews += [x.rating]

        for x in total_reviews:
            total += x
        avg = total / len(total_reviews)
        print(avg)

        if Mechanic_Ratings.query.first() is None:
            mechanic_reviews = Mechanic_Ratings(mechanic=form.mechanic.data, average=round(avg, 2))
            db.session.add(mechanic_reviews)
        else:
            for j in all_averages:
                if Mechanic_Ratings.query.filter_by(mechanic=form.mechanic.data) is None:
                    if j.mechanic == form.mechanic.data:
                        print("2nd if")
                        j.average = round(avg, 2)
                else:
                    print("else")
                    mechanic_reviews = Mechanic_Ratings(mechanic=form.mechanic.data, average=round(avg, 2))
                    db.session.add(mechanic_reviews)
        db.session.commit()

        return redirect(url_for('view_rating'))
    return render_template('MechanicRating.html', title='Review Mechanic', form=form)


@app.route('/view_reviews')
@login_required
def view_rating():
    mechanics_ratings = Mechanic_Ratings.query.all()
    all_reviews = Reviews.query.all()
    users = User.query.filter_by(role='Mechanic')
    return render_template('DisplayRatings.html', title='Mechanic Reviews', mechanics_ratings=mechanics_ratings,
                           all_reviews=all_reviews, users=users)


@app.route('/suggest_recommendations', methods=['GET', 'POST'])
@login_required
def suggest_recommendations():
    form = Suggestions()
    if form.validate_on_submit():
        recommendations_suggested = Recommendations(user=form.user.data, Tire_rotations=form.Tire_rotations.data,
                                                    Registration_update=form.Registration_update.data,
                                                    Change_break=form.Change_break.data, Car_Wash=form.Car_Wash.data,
                                                    Oil_change=form.Oil_change.data)
        db.session.add(recommendations_suggested)
        db.session.commit()

        return redirect(url_for('mechanicDashboard'))

    return render_template('Suggestions.html', title='Recommendations', form=form)


@app.route('/suggested_recommendations', methods=['GET', 'POST'])
@login_required
def recommendations():
    recommendations_made = Recommendations.query.all()
    return render_template('Suggestions_Proposed.html', title='Recommendations Made',
                           recommendations_made=recommendations_made)


@app.route('/payment', methods=['POST'])
def payment():
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"},
        "redirect_urls": {
            "return_url": "http://localhost:3000/payment/execute",
            "cancel_url": "http://localhost:3000/"},
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": "Service",
                    "sku": "12345",
                    "price": "50.00",
                    "currency": "USD",
                    "quantity": 1}]},
            "amount": {
                "total": "50.00",
                "currency": "USD"},
            "description": "Payment Transaction For Service."}]})

    if payment.create():
        print('Payment success!')
    else:
        print(payment.error)

    return jsonify({'paymentID': payment.id})


@app.route('/execute', methods=['POST'])
def execute():
    success = False
    payment = paypalrestsdk.Payment.find(request.form['paymentID'])

    if payment.execute({'payer_id': request.form['payerID']}):
        print('Execute success!')
        success = True
    else:
        print(payment.error)

    return jsonify({'success': success})
