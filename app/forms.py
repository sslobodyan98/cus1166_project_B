from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, DateField, TimeField, \
    SelectField
from wtforms.validators import DataRequired, ValidationError, EqualTo
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


class AddAvailability(FlaskForm):
    date = DateField('Date (year-month-date)', validators=[DataRequired()])
    start_time = TimeField('Start Time',validators=[DataRequired()])
    end_time= TimeField('End Time',validators=[DataRequired()])
    submit = SubmitField('Add')


class ScheduleAppointment(FlaskForm):
    date = DateField('Date (year-month-date)', validators=[DataRequired()])

    start_time = TimeField('Start Time',validators=[DataRequired()])
    # Mechanics=User.query.all()
    # for x in Mechanics:
    #     value=(x.user,x.user)
    mechanic = SelectField('Mechanics',
                           choices=[("John Doe", "John"), ("Dug Smith", "Dug"), ("Walter Green", "Walter")],
                           validators=[DataRequired()])
    submit = SubmitField('Add')
