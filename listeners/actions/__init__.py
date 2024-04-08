import re
from .login_button import login_button
from .delete_task import delete_task_action
from .register_button import register_button
from .refresh_home import refresh_home
from .home_task_status import home_task_status
from .search_tasks import search_tasks
from .task_detail_modal import task_detail_modal
from .task_details_from_message import task_details_from_message
from .home_project import home_project, home_personal_project
from .task_modal import update_task_modal, create_task_modal, task_modal_due_date_selector, task_modal_assignee_selector, task_modal_status_selector

def register(app):
    app.action("task_modal_assignee_selector")(task_modal_assignee_selector)
    app.action("task_modal_due_date_selector")(task_modal_due_date_selector)
    app.action("task_modal_status_selector")(task_modal_status_selector)
    app.action("min_due_date")(task_modal_due_date_selector)
    app.action("max_due_date")(task_modal_due_date_selector)
    app.action("min_created_date")(task_modal_due_date_selector)
    app.action("min_created_date")(task_modal_due_date_selector)
    app.action("login_button")(login_button)
    app.action("register_button")(register_button)
    app.action("refresh_home")(refresh_home)
    app.action("create_task")(create_task_modal)
    app.action("search_tasks")(search_tasks)
    app.action(re.compile("delete_task-(.+)"))(delete_task_action)
    app.action(re.compile("home_task_status-(.+)"))(home_task_status)
    app.action(re.compile("task_detail_modal-(.+)"))(task_detail_modal)
    app.action(re.compile("view_task_from_message"))(task_details_from_message)
    app.action(re.compile("home_project-(.+)"))(home_project)
    app.action("home_personal_project")(home_personal_project)
    app.action(re.compile("update_task_modal-(.+)"))(update_task_modal)