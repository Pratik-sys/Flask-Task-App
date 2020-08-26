from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextField, validators
from Todo.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', [validators.data_required(), validators.Length(max=25)])
    email = StringField('Email', [validators.data_required()])
    password = PasswordField('Password', [validators.data_required()])
    submit = SubmitField('Sign up')

class LoginForm(FlaskForm):
    email = StringField('Email', [validators.data_required()])
    password = PasswordField('Password', [validators.data_required()])
    submit = SubmitField('Login')

