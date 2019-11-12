'''
Created Oil Change Form

Taking mileage/update_miles out of Edit Vehilce, will be done in Oil Change

'''
from flask_wtf import FlaskForm, Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
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

class OilChangeForm(FlaskForm):
    mileage = IntegerField('Mileage at last oil change: ', validators=[DataRequired()]) #input field #default value = Car.mileage
    update_miles = IntegerField('Current Mileage: ') #input field #default value = Car.update_miles
    miles_until_next_oil_change = IntegerField('Miles Until Next Oil Change') #data not required, will be filled in #make view only field
    submit = SubmitField('Submit') #bind this to the method that calculates miles_until_next_oil_change
