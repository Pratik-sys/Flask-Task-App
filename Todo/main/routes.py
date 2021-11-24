from flask import render_template, Blueprint
from Todo.models import Todo
from flask_login import login_required

main = Blueprint("main", __name__)


@main.route("/")
@login_required
def home():
    try:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template("home.html", tasks=tasks)
    except Exception as ex:
        return (f"Noting to list {ex}"), 500
