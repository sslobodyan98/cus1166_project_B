from flask_wtf import FlaskForm, Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User


class LoginForm(FlaskForm):
    user = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class AddVehicle(Form):
    car_vin = StringField('VIN Number', validators=[DataRequired])
    make = StringField('Make', validators=[DataRequired()])
    model = StringField('Model', validators=[DataRequired()])
    color = StringField('Color', validators=[DataRequired])
    mileage = IntegerField('Mileage', validators=[DataRequired])
    submit = SubmitField('Submit')


class RegistrationForm(FlaskForm):
    user = StringField('User', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired])
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
