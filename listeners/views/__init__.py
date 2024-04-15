import re
from .submit_new_task import submit_new_task
from .submit_create_project import submit_create_project
from .submit_delete_task import submit_delete_task
from .submit_update_task import submit_update_task
from .login import login
from .register import submit_register
from .search_tasks import search_tasks

def register(app):
    app.view("submit_new_task")(submit_new_task)
    app.view(re.compile("submit_new_task-(.+)"))(submit_new_task)
    app.view("submit_create_project")(submit_create_project)
    app.view("login")(login)
    app.view("submit_register")(submit_register)
    app.view("search_tasks")(search_tasks)
    app.view(re.compile("delete_task-(.+)"))(submit_delete_task)
    app.view(re.compile("update_task-(.+)"))(submit_update_task)
