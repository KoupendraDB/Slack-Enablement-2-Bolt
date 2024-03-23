from .assignee_selector import assignee_selector
from .due_date_selector import due_date_selector
from .login_button import login_button

def register(app):
    app.action("assignee_selector")(assignee_selector)
    app.action("due_date_selector")(due_date_selector)
    app.action("login_button")(login_button)