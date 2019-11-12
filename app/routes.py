'''
Created route for Oil Change Form

Taking mileage/update_miles out of Edit Vehicle, will be done in Oil Change
'''
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, AddVehicle, RegistrationForm, EditVehicleForm, OilChangeForm
from app.models import User, Car
from app.miles_utils import oil_change_calculation


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
        db.session.commit()
        flash('Your vehicle changes have been saved')
        return redirect(url_for('editVehicle'))
    elif request.method == 'GET':
        form.car_vin.data = current_user.car_vin
        form.make.data = current_user.make
        form.model.data = current_user.model
        form.color.data = current_user.color
    return render_template('editVehicle.html', title='Edit Vehicle',
                           form=form)

@app.route('/oil_change', methods=['GET', 'POST'])
@login_required
def OilChange():
    form = OilChangeForm()
    if form.validate_on_submit(): #if submit button is pressed

        miles_until_next_oil_change, oil_change_required = oil_change_calculation()

        if oil_change_required: #if oil_change_required is True
            flash('Miles left until your next oil change: ' + miles_until_next_oil_change + ', you need an oil change.')
        elif not oil_change_required: #if oil_change_required is False
            flash('Miles left until your next oil change: ' + miles_until_next_oil_change
                  + ', you do not need an oil change.')

        return redirect(url_for('oil_change'))
    return render_template('oil_change.html', title='Oil Change', form=form)
    #render vs redirect?


