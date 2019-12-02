from flask import flash
from flask_wtf import FlaskForm, Form


from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, RadioField, DateField,\
    TimeField, SelectField
from wtforms.validators import DataRequired, ValidationError, EqualTo

from app.models import User, Car


class LoginForm(FlaskForm):
    user = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

    def get_role(self, role):
        role = User.query.filter_by(role=role.data).first()
        if role is not None:
            raise ValidationError('Please select a role')




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

class DeleteVehicleForm(FlaskForm):
    car_info = StringField('VIN Number', validators=[DataRequired()])
    submit = SubmitField('Delete')


class RegistrationForm(FlaskForm):
    user = StringField('User', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    role = RadioField('Who are you?', choices=[('Car Owner', 'Car Owner'), ('Mechanic', 'Mechanic')],
                      validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_user(self, user):
        user = User.query.filter_by(user=user.data).first()
        if user is not None:
            raise ValidationError('Please use a different name')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email')


class AddAvailability(FlaskForm):
    date = DateField('Date (year-month-date)', validators=[DataRequired()])
    start_time = TimeField('Start Time', validators=[DataRequired()])
    end_time = TimeField('End Time', validators=[DataRequired()])
    submit = SubmitField('Add')


class ScheduleAppointment(FlaskForm):
    vehicle = StringField('Which Car', validators=[DataRequired()])
    date = DateField('Date (year-month-date)', validators=[DataRequired()])
    start_time = TimeField('Start Time', validators=[DataRequired()])
    mechanic = StringField('Mechanics',validators=[DataRequired()])

    submit = SubmitField('Add')


class EditAppointmentForm(FlaskForm):
    date = DateField('Update Date (year-month-date)', validators=[DataRequired()])
    start_time = TimeField('Update Start Time', validators=[DataRequired()])
    submit = SubmitField('Update')

class OilChangeForm(FlaskForm):
    car = StringField('Which car', validators=[DataRequired()])
    update_miles = IntegerField('Current Mileage: ') #input field #default value = Car.update_miles
    submit = SubmitField('Submit') #bind this to the method that calculates miles_until_next_oil_change


class DeleteAppointmentForm(FlaskForm):
    date = DateField('Date (year-month-date)', validators=[DataRequired()])
    start_time = TimeField('Start Time', validators=[DataRequired()])
    mechanic = StringField('Mechanics',validators=[DataRequired()])
    car = StringField('Car', validators=[DataRequired()])
    submit = SubmitField('Delete')

