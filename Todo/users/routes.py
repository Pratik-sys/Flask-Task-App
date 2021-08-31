from flask import (
    render_template,
    url_for,
    request,
    redirect,
    flash,
    make_response,
    jsonify,
    Blueprint,
)
from Todo import db, bcrypt
import bleach
from Todo.models import User, Todo
from Todo.users.forms import RegistrationForm, LoginForm
from flask_login import login_user, current_user, logout_user

users = Blueprint("users", __name__)


@users.route("/signup", methods=["POST", "GET"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = RegistrationForm(request.form)
    if request.method == "POST" and form.validate():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        user = User(
            username=bleach.clean(form.username.data),
            email=form.email.data,
            password=hashed_password,
        )
        db.session.add(user)
        db.session.commit()
        flash("Account has been created successfully!", "success")
        return redirect(url_for("users.login"))
    return render_template("register.html", form=form)


@users.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = LoginForm(request.form)
    if request.method == "POST" and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash("Logged in Successfully", "success")
            return redirect(url_for("main.home"))
        else:
            flash(
                "The Account dosen't match, please check your email and password again",
                "warning",
            )
    return render_template("login.html", form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.home"))


@users.route("/getValues", methods=["POST"])
def getValues():
    req = request.get_json(force=True)
    task = Todo.query.get_or_404(req["value"])
    task.flag = req["Flag"]
    db.session.commit()
    res = make_response(jsonify(req), 200)
    return res
