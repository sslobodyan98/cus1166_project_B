from flask import flash
from flask_wtf import FlaskForm, Form


from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, RadioField, DateField,\
    TimeField, SelectField, DecimalField, DateTimeField
from wtforms.validators import DataRequired, ValidationError, EqualTo
from datetime import datetime
from datetime import date
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
    registration_date = DateField('Last Registration Date (year-month-date)', validators=[DataRequired()]
                                  , format='%Y-%m-%d', default=date.today())
    submit = SubmitField('Submit')

    def validate_car_vin(self, car_vin):
        car_vin = Car.query.filter_by(car_vin=car_vin.data).first()
        if car_vin is not None:
            raise ValidationError('Please use a different VIN')


class DeleteVehicleForm(FlaskForm):
    make = StringField('Enter make to delete', validators=[DataRequired()])
    model = StringField('Enter model to delete', validators=[DataRequired()])
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
    mechanic = StringField('Mechanics', validators=[DataRequired()])
    appointment_type = SelectField(choices=[('Oil Change', 'Oil Change'), ('Tire Rotation', 'Tire Rotation'),
                                            ('Registration', 'Registration'), ('Break Change', 'Break Change'),
                                            ('Car Wash', 'Car Wash')], validators=[DataRequired()])
    submit = SubmitField('Add')


class EditAppointmentForm(FlaskForm):
    date = DateField('Update Date (year-month-date)', validators=[DataRequired()])
    start_time = TimeField('Update Start Time', validators=[DataRequired()])
    submit = SubmitField('Update')


class OilChangeForm(FlaskForm):
    car = StringField('Which car', validators=[DataRequired()])
    update_miles = IntegerField('Current Mileage: ')  # input field #default value = Car.update_miles
    submit = SubmitField('Submit')  # bind this to the method that calculates miles_until_next_oil_change


class DeleteAppointmentForm(FlaskForm):
    date = DateField('Date (year-month-date)', validators=[DataRequired()])
    start_time = TimeField('Start Time', validators=[DataRequired()])
    mechanic = StringField('Mechanics', validators=[DataRequired()])
    car = StringField('Car', validators=[DataRequired()])
    submit = SubmitField('Delete')


class ReviewMechanic(FlaskForm):
    mechanic = StringField('Mechanic name', validators=[DataRequired()])
    rating = DecimalField('Rating from 0-5', validators=[DataRequired()])
    comments = StringField('Mechanic name', validators=[DataRequired()])
    submit = SubmitField('Submit')


class Suggestions(FlaskForm):
    user = StringField('Who is the user', validators=[DataRequired()])
    Tire_rotations = RadioField('Does the customer need a tire rotation', choices=[('Yes', 'Yes'), ('No', 'No')],
                                validators=[DataRequired()])
    Registration_update = RadioField('Does the customer need a registration update',
                                     choices=[('Yes', 'Yes'), ('No', 'No')],
                                     validators=[DataRequired()])
    Change_break = RadioField('Does the customer need their breaks changed', choices=[('Yes', 'Yes'), ('No', 'No')],
                              validators=[DataRequired()])
    Car_Wash = RadioField('Does the customer need a car wash', choices=[('Yes', 'Yes'), ('No', 'No')],
                          validators=[DataRequired()])
    Oil_change = RadioField('Does the customer need an oil change', choices=[('Yes', 'Yes'), ('No', 'No')],
                            validators=[DataRequired()])
    submit = SubmitField('Submit')

# class ConfirmAppointmentCompletedForm(FlaskForm):
#     confirm_service = StringField('Confirm Service Performed', default='Done')
#     submit = SubmitField('Confirm Service Performed')

# Confirm_appointmentchoices = ('Service Completed', 'Service Incomplete', 'Service Denied',
#                               'Did not show up to appointment')
#
#
# class ConfirmAppointmentCompletedForm(FlaskForm):
#     confirm_service = SelectField(label='Choice', choices=[(confirm_service, confirm_service) for
#                                                            confirm_service in Confirm_appointmentchoices])
#     submit = SubmitField('Confirm Appointment Status')
#
#
# Confirm_paymentstatuschoices = ('Paid', 'Unpaid', 'Missing balance')
#
#
# class ConfirmAppointmentPaidForm(FlaskForm):
#     confirm_paid = SelectField(label='Choice', choices=[(confirm_paid, confirm_paid) for
#                                                         confirm_paid in Confirm_paymentstatuschoices])
#     submit = SubmitField('Confirm Payment Status')

class ConfirmAppointmentCompletedForm(FlaskForm):
    confirm_service = SelectField('Choice', [DataRequired()],
                                  choices=[('Service Completed', 'Service Completed'),
                                           ('Service Incomplete', 'Service Incomplete'),
                                           ('Service Denied', 'Service Denied'),
                                           ('Did not show up to appointment', 'Did not show up to appointment')])

    submit = SubmitField('Confirm Appointment Status')


class ConfirmAppointmentPaidForm(FlaskForm):
    confirm_paid = SelectField('Choice', [DataRequired()],
                               choices=[('Paid', 'Paid'),
                                        ('Unpaid', 'Unpaid'),
                                        ('Missing Balance', 'Missing Balance')])

    submit = SubmitField('Confirm Payment Status')