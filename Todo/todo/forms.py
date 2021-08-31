from wtforms import Form, StringField, SubmitField, PasswordField, TextField, validators, ValidationError

class PostForm(Form):
    content = TextField('Add Task', [validators.data_required()])
    submit = SubmitField('Post')
