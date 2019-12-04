from flask_wtf import FlaskForm, Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class AddVehicle(Form):
    make = StringField('Make', validators=[DataRequired()])
    model = StringField('Model', validators=[DataRequired()])
    submit = SubmitField('Submit')

# class RegistrationForm(Form):
#     make = StringField('make', validators=[DataRequired()])
#     model = StringField('model', validators=[DataRequired()])
    #color = StringField('New Password', validators=[DataRequired()])
