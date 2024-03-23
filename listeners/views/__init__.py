from .submit_new_task import submit_new_task
from .login import login

def register(app):
    app.view("submit_new_task")(submit_new_task)
    app.view("login")(login)
