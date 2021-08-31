import random, string
class Config:
    SECRET_KEY = "".join(
        random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits)
        for _ in range(16)
    )
    SQLALCHEMY_DATABASE_URI = 'sqlite:///Todo.db' # set the congif where you want to save the db 
    SQLALCHEMY_TRACK_MODIFICATIONS= False