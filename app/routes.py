import datetime
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from flask_mail import Mail, Message
from app import app, db
from app.forms import LoginForm, AddVehicle, RegistrationForm, OilChangeForm, AddAvailability, ScheduleAppointment, \
    EditAppointmentForm
from app.models import User, Car, Availability, Schedules

now = datetime.datetime.now()
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
    if form.validate_on_submit():
        car = Car(user=current_user.user, car_vin=form.car_vin.data, make=form.make.data, model=form.model.data,
                  color=form.color.data, mileage=form.mileage.data)
        db.session.add(car)
        db.session.commit()
        if user.role == 'Car Owner' and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('index'))
        elif user.role == 'Mechanic' and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('mechanicDashboard'))
    return render_template('addVehicle.html', title='Add Vehicle', form=form)


@app.route('/addAvailability', methods=['GET', 'POST'])
def addAvailability():
    form = AddAvailability()
    if form.validate_on_submit():
        time = Availability(user=current_user.user, date=form.date.data, start_time=form.start_time.data,
                            end_time=form.end_time.data)
        db.session.add(time)
        db.session.commit()
        if user.role == 'Car Owner' and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('index'))
        elif user.role == 'Mechanic' and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('mechanicDashboard'))
    return render_template('Mechanic_AvaialablityForm.html', title='Add availability', form=form)


@app.route('/ScheduleAppointment', methods=['GET', 'POST'])
def Schedule():
    form = ScheduleAppointment()
    mechanics = User.query.filter_by(role='Mechanic')
    if form.validate_on_submit():
        Scheduled = Schedules.query.all()
        Availabilitys = Availability.query.all()
        for x in Scheduled:
            if x.appointment_date == form.date.data and x.appointment_time == form.start_time.data and x.mechanic == form.mechanic.data:
                flash("Appointment can't be made because the time or mechanic is not available")
        for i in Availabilitys:
            if i.mechanic == form.Mechanics.data and i.date == form.date.data and (
                    form.start_time.data < i.start_time or form.start_time.data > i.end_time):
                flash("Appointment can't be made because the time or mechanic is not available")

        for x in Scheduled:
            diff = x.appointment_date - datetime.date.today()
            if diff.days > 3:  # check for 5 days
                msg = Message('Appointment Reminder Notification', recipients=[current_user.email])
                msg.body = 'Hello, You have an appointment scheduled in 3 days. We hope to see you!'
                msg.html = '<p>You have an appointment scheduled in 3 days</p>'
                mail.send(msg)

        meeting = Schedules(user=current_user.user, mechanic=form.mechanic.data, appointment_date=form.date.data,
                            appointment_time=form.start_time.data)
        db.session.add(meeting)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('ScheduleAppointment.html', title='Schedule Appointment', form=form, mechanics=mechanics)


@app.route('/EditAppointment', methods=['GET', 'POST'])
def editAppointment():
    form = EditAppointmentForm()
    if form.validate_on_submit():
        appointmentsMade = Schedules.query.all()
        for x in appointmentsMade:
            if x.appointment_date == form.date.data and x.appointment_time == form.start_time.data:
                return redirect(url_for('editAppointments'))
            elif current_user.user == x.user and form.date.data == x.appointment_date:
                x.appointment_time = form.start_time.data
                db.session.commit()
                return redirect(url_for('index'))

    return render_template('EditApt.html', title='Edit Appointment', form=form)


@app.route('/DisplayAvailability', methods=['GET', 'POST'])
def DisplayAvailabilities():
    Availabilities = Availability.query.all()
    ScheduledAppointments = Schedules.query.all()
    return render_template('DisplayMechanicAvailability.html',
                           Availabilities=Availabilities, ScheduledAppointments=ScheduledAppointments)


@app.route('/oil_change', methods=['GET', 'POST'])
@login_required
def OilChange():
    form = OilChangeForm()
    cars = Car.query.all()
    if form.validate_on_submit():  # if submit button is pressed

        difference = form.update_miles.data - form.mileage.data
        if difference < 5000:
            miles_until_next = 5000 - form.update_miles.data
            return "You dont need one"
        elif difference >= 5000:
            msg = Message('Oil Change Reminder Notification', recipients=[current_user.email])
            msg.body = 'Hi, Its time for you to schedule your next car maintenance appointment as your oil needs to ' \
                       'be changed! '
            msg.html = '<b>This is a Reminder Notification </b>'
            mail.send(msg)
            return "You need an oil change"
    return render_template('oil_change.html', title='Oil Change', form=form, cars=cars)


@app.route('/mechanicDashboard')
@login_required
def mechanicDashboard():
    cars = Car.query.all()
    schedules = Schedules.query.all()
    return render_template('mechanicDashboard.html', title='Mechanic Dashboard', cars=cars, schedules=schedules)
