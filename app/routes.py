import datetime
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from flask_mail import Mail, Message
from app import app, db
from app.forms import LoginForm, AddVehicle, RegistrationForm, OilChangeForm, AddAvailability, ScheduleAppointment, \
    EditAppointmentForm, DeleteAppointmentForm, ResetPasswordForm
from app.models import User, Car, Availability, Schedules

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
# app.config['MAIL_SUPPRESS_SEND'] = False
app.config['MAIL_ASCII_ATTATCHMENTS'] = False

mail = Mail(app)


@app.route('/')
@app.route('/index')
@login_required
def index():
    cars = Car.query.all()
    appointments = Schedules.query.all()
    appointments = Schedules.query.all()
    for x in appointments:
        diff = x.appointment_date - datetime.date.today()
        if diff.days == 3:
            msg = Message('Appointment Reminder Notification', recipients=[current_user.email])
            msg.body = 'Hello, You have an appointment scheduled in 3 days. We hope to see you!'
            msg.html = '<p>You have an appointment scheduled in 3 days</p>'
            mail.send(msg)
        elif diff.days < 1:
            msg = Message('Follow up for oil change appointment', recipients=[current_user.email])
            msg.body = ''
            msg.html = 'Hello, I hope your appointment went well. If you could please take the brief survey and review ' \
                       'your mechanic we would highly appreciate it. <a ' \
                       'href="http://127.0.0.1:5000/review_appointment"> Click here to access review</a> '
            mail.send(msg)
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
'''
@app.route('/forgot_password', methods=['GET', 'POST'])
def ForgotPassword():
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        msg = Message('Reset Password', recipients=[current_user.email])
        msg.body = 'Click the link below to reset your password:' '(link)'
        msg.html = '<b>Reset Password</b>'
        mail.send(msg)
        #return redirect(url_for('ResetPassword'))
    return render_template('forgot_password.html', title='forgot_password', form=form) #users=users?
'''
@app.route('/resetPassword', methods=['GET', 'POST'])
def ResetPassword():
    form = ResetPasswordForm()
    if form.validate_on_submit():
        #user = current_user #?
        db.session.delete(user.password_hash)  # delete old password
        user.set_password(form.password.data) # get new password data that they entered
        #add new password to db ?
        db.session.commit()  # commit changes
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
    if form.validate_on_submit():
        car = Car(user=current_user.user, car_vin=form.car_vin.data, make=form.make.data, model=form.model.data,
                  color=form.color.data, mileage=form.mileage.data)
        db.session.add(car)
        db.session.commit()
        flash('You have added a car to use in our App!')
        return redirect(url_for('index'))
    return render_template('addVehicle.html', title='Add Vehicle', form=form)


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

    mechanics = User.query.filter_by(role='Mechanic')
    availabilities = Availability.query.all()
    if form.validate_on_submit():
        appointments = Schedules.query.all()
        for x in appointments:

            if x.appointment_date == form.date.data and x.appointment_time == form.start_time.data and \
                    x.mechanic == form.mechanic.data:
                return redirect(url_for('Schedule'))
        for i in availabilities:
            if i.user == form.mechanic.data and i.date == form.date.data and (form.start_time.data < i.start_time or
                                                                              form.start_time.data > i.end_time):
                return redirect(url_for('Schedule'))
        for i in availabilities:
            if i.user == form.mechanic.data and i.date == form.date.data and (
                    form.start_time.data < i.start_time or form.start_time.data > i.end_time):
                return redirect(url_for('Schedule'))
        meeting = Schedules(user=current_user.user, mechanic=form.mechanic.data, appointment_date=form.date.data,
                            appointment_time=form.start_time.data, vehicle=form.vehicle.data)
        db.session.add(meeting)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('ScheduleAppointment.html', title='Schedule Appointment', form=form, mechanics=mechanics)


@app.route('/EditAppointment', methods=['GET', 'POST'])
def editAppointment():
    form = EditAppointmentForm()
    if form.validate_on_submit():
        appointments = Schedules.query.all()
        for x in appointments:
            if x.appointment_date == form.date.data and x.appointment_time == form.start_time.data:
                return redirect(url_for('editAppointments'))
            elif current_user.user == x.user and form.date.data == x.appointment_date:
                x.appointment_time = form.start_time.data
                db.session.commit()
                return redirect(url_for('index'))

    return render_template('EditApt.html', title='Edit Appointment', form=form)


@app.route('/DeleteAppointment', methods=['GET', 'POST'])
def deleteAppointment():
    form = DeleteAppointmentForm()
    if form.validate_on_submit():
        appointments = Schedules.query.all()
        for x in appointments:
            if x.appointment_date == form.date.data and x.appointment_time == form.start_time.data and x.mechanic == form.mechanic.data and x.vehicle == form.car.data:
                db.session.delete(x)
                db.session.commit()
                return redirect(url_for('index'))

    return render_template('delete_appointment.html', title='Edit Appointment', form=form)


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
                x.mileage = form.update_miles.data
                x.miles_until_oil_change = 5000 - form.update_miles.data
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


@app.route('/mechanicDashboard')
@login_required
def mechanicDashboard():
    appointments = Schedules.query.all()
    return render_template('mechanicDashboard.html', title='Mechanic Dashboard', appointments=appointments)
