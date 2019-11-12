#adding appointment_date to Edit Vehicle

#made form for in-app notifications
from datetime import datetime

from flask import flash
from flask_wtf import FlaskForm, Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo

from app import db
from app.models import User, Car


class LoginForm(FlaskForm):
    user = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class AddVehicle(FlaskForm):
    car_vin = StringField('VIN Number', validators=[DataRequired()])
    make = StringField('Make', validators=[DataRequired()])
    model = StringField('Model', validators=[DataRequired()])
    color = StringField('Color', validators=[DataRequired()])
    mileage = IntegerField('Mileage', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def validate_car_vin(self, car_vin):
        car_vin = Car.query.filter_by(car_vin=car_vin.data).first()
        if car_vin is not None:
            raise ValidationError('Please use a different VIN')


class EditVehicleForm(FlaskForm):
    car_vin = StringField('VIN Number', validators=[DataRequired()])
    make = StringField('Make', validators=[DataRequired()])
    model = StringField('Model', validators=[DataRequired()])
    color = StringField('Color', validators=[DataRequired()])
    mileage = IntegerField('Mileage', validators=[DataRequired()])
    appointment_date = db.Column(db.datetime) #adding appointment_date
    submit = SubmitField('Submit')


class RegistrationForm(FlaskForm):
    user = StringField('User', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_user(self, user):
        user = User.query.filter_by(user=user.data).first()
        if user is not None:
            raise ValidationError('Please use a different name')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email')

class AppNotificationForm(FlaskForm): #notifications in App, printing appointment info
    for car in User.cars:
        delta = car.appointment_date - datetime.datetime.now().date()  # appointment_date is field in Car table
        if delta.days <= 3: #notification stays up until day of appointment
            # if appointment is in 3 days (only sent on 3rd day before appointment)
            flash('You have an appointment scheduled on ' + car.appointment_date)
            flash('Vehicle: ' + car.car_vin + ', ' + car.make + ', ' + car.model + ', ' + car.color )