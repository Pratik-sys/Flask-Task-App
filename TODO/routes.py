from flask import render_template,url_for,request,redirect, flash 
from Todo import app, db, bcrypt
from Todo.models import Todo, User
from Todo.forms import RegistrationForm, LoginForm
from flask_login import login_user, current_user,logout_user, login_required

@app.route('/', methods=['POST', 'GET'])
@login_required
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'Error while adding task'
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)

@app.route('/delete/<int:id>')
@login_required

def delete(id):
    task_del = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_del)
        db.session.commit()
        return redirect('/')
    except:
        return "Error in deleting the task"
    
@app.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required

def update(id):
    task_update = Todo.query.get_or_404(id)
    if request.method == "POST":
        task_update.content = request.form['content']
        
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "Issue in updating the task"

    else:
        return render_template('update.html', task_update = task_update)

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm(request.form)
    if  form.validate():
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
        return redirect(url_for('index'))

    form = LoginForm(request.form)
    if  form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Logged in Successfully', 'success')
            return redirect(url_for('index'))
    return render_template('login.html', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))