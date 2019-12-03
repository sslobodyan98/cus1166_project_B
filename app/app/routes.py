from flask import render_template, flash, redirect, url_for
from app import app
from app.models import *
from app.forms import LoginForm, AddVehicle


@app.route('/')
@app.route('/index')
def index():
    user = {'user_name': 'Tom'}
    cars = [
        {
            'owner': {'user_name': 'John'},
            'car': 'Testing Car String'
        },
        {
            'owner': {'user_name': 'Doe'},
            'car': 'Testing Car String2'
        }
    ]
    return render_template('index.html', title='Home', user=user, cars=cars)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.is_submitted():
        username= form.username.data
        newUser = User(id=16,user=username,email="firstname.last@google.com")
        db.session.add(newUser)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('login.html',  title='Sign In', form=form)

# @app.route('/add_vehicle', methods=['GET', 'POST']) #### Not Working Yet
# def add_vehicle():
#     form = AddVehicle()
#     if form.validate_on_submit():
#         flash('Add requested for car {}, remember_me={}'.format(
#             form.make.data, form.model.data))
#         return redirect(url_for('index'))
#     return render_template('addVehicle.html',  title='Add Vehicle', form=form)

@app.route('/addVehicle', methods=['GET', 'POST'])
def RegisterCar():
    form = AddVehicle()
    if form.is_submitted():
        models = form.model.data
        newModel = Car(id=126, car_vin="126",make='ik',model=models,color='blue',mileage=13,owner_id=16)
        db.session.add(newModel)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('addVehicle.html',  title='Add Vehicle', form=form)
