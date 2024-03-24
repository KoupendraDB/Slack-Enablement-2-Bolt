import re
from .assignee_selector import assignee_selector
from .due_date_selector import due_date_selector
from .login_button import login_button
from .home_assignee_selector import home_assignee_selector
from .task_status_selector import task_status_selector
from .register_button import register_button

def register(app):
    app.action("assignee_selector")(assignee_selector)
    app.action("due_date_selector")(due_date_selector)
    app.action("login_button")(login_button)
    app.action("register_button")(register_button)
    app.action(re.compile("assignee_selector-(.+)"))(home_assignee_selector)
    app.action(re.compile("task_status_selector-(.+)"))(task_status_selector)