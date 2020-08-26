from flask import render_template,url_for,request,redirect
from Todo import app, db
from Todo.models import Todo
from Todo.forms import RegistrtionForm, LoginForm

@app.route('/', methods=['POST', 'GET'])
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
def delete(id):
    task_del = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_del)
        db.session.commit()
        return redirect('/')
    except:
        return "Error in deleting the task"
    
@app.route('/update/<int:id>', methods=['GET', 'POST'])
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

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegistrtionForm()
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('login.html', form=form)
