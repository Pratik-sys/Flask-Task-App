from flask import render_template,url_for,request,redirect, flash
from Todo import app, db, bcrypt
from Todo.models import Todo, User
from Todo.forms import RegistrationForm, LoginForm, PostForm 
from flask_login import login_user, current_user,logout_user, login_required

@app.route("/home")
@app.route("/")
@login_required
def home():
    tasks = Todo.query.order_by(Todo.date_created).all()
    return render_template('home.html', tasks=tasks)

@app.route('/delete/<int:id>')
@login_required

def delete(id):
    task_del = Todo.query.get_or_404(id)
    db.session.delete(task_del)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))
    
@app.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
    form = PostForm(request.form)
    post = Todo.query.get_or_404(id)
    if form.validate():
        post.content = form.content.data
        db.session.commit()
        flash('Task Updated', 'success')
        return redirect(url_for('home'))
    elif request.method == 'GET':
        form.content.data = post.content
    return render_template('update.html', form=form)


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistrationForm(request.form)
    if request.method =='POST' and  form.validate():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash("Account has been created successfully!", "success")
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm(request.form)
    if request.method =='POST' and  form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Logged in Successfully', 'success')
            return redirect(url_for('home'))
        else:
            flash("The Account dosen't match, please check your email and password again", "warning")
    return render_template('login.html', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/post", methods=['POST','GET'])
def post():
    form = PostForm(request.form)
    if form.validate():
        task = Todo(content=form.content.data, author=current_user)
        db.session.add(task)
        db.session.commit()
        flash('Task Posted!', 'success')
        return redirect(url_for('home'))
    return render_template('post.html', form=form)