from flask import render_template, url_for, flash, Blueprint
from Todo.models import Todo
from flask_login import login_required

main = Blueprint("main", __name__)


@main.route("/home")
@main.route("/")
@login_required
def home():
    tasks = Todo.query.order_by(Todo.date_created).all()
    return render_template("home.html", tasks=tasks)
