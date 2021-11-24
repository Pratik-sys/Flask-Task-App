from wtforms import Form, SubmitField, TextAreaField, validators


class PostForm(Form):
    content = TextAreaField("Add Task", [validators.data_required()])
    submit = SubmitField("Post")
