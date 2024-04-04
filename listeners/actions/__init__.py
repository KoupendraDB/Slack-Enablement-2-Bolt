import re
from .assignee_selector import assignee_selector
from .due_date_selector import due_date_selector
from .login_button import login_button
from .home_assignee_selector import home_assignee_selector
from .task_status_selector import task_status_selector
from .task_eta_selector import task_eta_selector
from .delete_task import delete_task_action
from .task_details import task_details
from .register_button import register_button
from .refresh_home import refresh_home
from .home_task_status import home_task_status
from .create_task import create_task
from .search_tasks import search_tasks
from .task_detail_modal import task_detail_modal
from .task_details_from_message import task_details_from_message

def register(app):
    app.action("assignee_selector")(assignee_selector)
    app.action("due_date_selector")(due_date_selector)
    app.action("min_due_date")(due_date_selector)
    app.action("max_due_date")(due_date_selector)
    app.action("min_created_date")(due_date_selector)
    app.action("min_created_date")(due_date_selector)
    app.action("login_button")(login_button)
    app.action("register_button")(register_button)
    app.action("refresh_home")(refresh_home)
    app.action("create_task")(create_task)
    app.action("search_tasks")(search_tasks)
    app.action(re.compile("assignee_selector-(.+)"))(home_assignee_selector)
    app.action(re.compile("task_status_selector-(.+)"))(task_status_selector)
    app.action(re.compile("task_eta_selector-(.+)"))(task_eta_selector)
    app.action(re.compile("delete_task-(.+)"))(delete_task_action)
    app.action(re.compile("task_details-(.+)"))(task_details)
    app.action(re.compile("home_task_status-(.+)"))(home_task_status)
    app.action(re.compile("task_detail_modal-(.+)"))(task_detail_modal)
    app.action(re.compile("view_task_from_message"))(task_details_from_message)