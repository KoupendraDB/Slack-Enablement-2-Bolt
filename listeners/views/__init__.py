from .submit_new_task import submit_new_task
from .login import login
from .register import submit_register

def register(app):
    app.view("submit_new_task")(submit_new_task)
    app.view("login")(login)
    app.view("submit_register")(submit_register)
