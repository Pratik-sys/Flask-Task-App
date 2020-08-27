# from flask_wtf import FlaskForm
from wtforms import Form, StringField, SubmitField, PasswordField, TextField, validators
from Todo.models import User

class RegistrationForm(Form):
    username = StringField('Username', [validators.data_required(), validators.Length(max=25)])
    email = StringField('Email', [validators.data_required()])
    password = PasswordField('Password', [validators.data_required()])
    submit = SubmitField('Sign up')

class LoginForm(Form):
    email = StringField('Email', [validators.data_required()])
    password = PasswordField('Password', [validators.data_required()])
    submit = SubmitField('Login')

class PostForm(Form):
    content = TextField('Add Task', [validators.data_required()])
    submit = SubmitField('Post')
