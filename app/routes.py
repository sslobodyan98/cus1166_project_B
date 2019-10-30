from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, AddVehicle, RegistrationForm
from app.models import User, Car


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
    # if form.validate_on_submit():
    #     flash('Vehicle addition requested for car_vin {}, make {}, model {}, color {},
    #     mileage {}'.format(
    #         form.car_vin.data, form.make.data, form.model.data, form.color.data
    #         form.mileage.data))
    #     return redirect(url_for('index'))
    return render_template('addVehicle.html', title='Add Vehicle', form=form)












# @app.route('/new_Car', methods=['GET', 'POST'])
# def new_Car():
#     """
#     ADD NEW CAR
#
#     """
#     form = AddVehicle(request.form)
#
#
#     if request.method == 'POST' and form.validate():
#
#         car = AddVehicle()
#         save_changes(car, form, new=True)
#         flash('Car added successfully!')
#         return redirect('/')
#
#     return render_template('addVehicle.html', form=form)
#
# def save_changes(car, form, new=False):
#     """
#     Save changes to db
#     """
#     #Get data from form and assign it to correct attributes
#     #of the SQLAlchemy table object
#     car_vin = CarVin()
#     car_vin.info = form.car_vin.data
#
#     car.car_vin = car_vin
#     car.make = form.make.data
#     car.model = form.model.data
#     car.color = form.color.data
#     car.mileage = form.mileage.data
#
#     if new:
#         db_session.add(car)
#         db_session.commit()