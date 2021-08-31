from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__) 
app.config['SECRET_KEY'] = 'ce93c0d66f7ea57ff4c6'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Todo.db' # set the congif where you want to save the db 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

from Todo.users.routes import users
from Todo.todo.routes import todos
from Todo.main.routes import main

app.register_blueprint(users)
app.register_blueprint(todos)
app.register_blueprint(main)
