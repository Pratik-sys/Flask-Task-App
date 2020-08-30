from wtforms import Form, StringField, SubmitField, PasswordField, TextField, validators, ValidationError
from Todo.models import User

class RegistrationForm(Form):
    username = StringField('Username', [validators.data_required(), validators.Length(max=25)])
    email = StringField('Email', [validators.data_required(), validators.Email()])
    password = PasswordField('Password', [validators.data_required()])
    submit = SubmitField('Sign up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

class LoginForm(Form):
    email = StringField('Email', [validators.data_required(), validators.Email()])
    password = PasswordField('Password', [validators.data_required()])
    submit = SubmitField('Login')

class PostForm(Form):
    content = TextField('Add Task', [validators.data_required()])
    submit = SubmitField('Post')
