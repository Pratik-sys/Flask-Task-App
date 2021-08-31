from flask import render_template,request,url_for,redirect, flash, Blueprint
from Todo import  db
import bleach
from Todo.models import Todo
from Todo.todo.forms import PostForm
from flask_login import current_user, login_required

todos = Blueprint('todos', __name__)

@todos.route('/delete/<int:id>')
@login_required

def delete(id):
    task_del = Todo.query.get_or_404(id)
    db.session.delete(task_del)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return render_template('home.html')
    
@todos.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
    form = PostForm(request.form)
    post = Todo.query.get_or_404(id)
    if form.validate():
        post.content = bleach.clean(form.content.data)
        db.session.commit()
        flash('Task Updated', 'success')
        return redirect(url_for('main.home'))
    elif request.method == 'GET':
        form.content.data = post.content
    return render_template('update.html', form=form)

@todos.route("/post", methods=['POST','GET'])
def post():
    form = PostForm(request.form)
    if form.validate():
        task = Todo(content=bleach.clean(form.content.data), author=current_user)
        db.session.add(task)
        db.session.commit()
        flash('Task Posted!', 'success')
        return redirect(url_for('main.home'))
    return render_template('post.html', form=form)