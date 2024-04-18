import re
from .login_button import login_button
from .delete_task import delete_task_action
from .refresh_home import refresh_home
from .home_task_status_filter import home_task_status
from .search_tasks import search_tasks
from .task_detail_modal import task_detail_modal
from .task_details_from_message import task_details_from_message
from .home_project_filter import home_project, home_personal_project
from .task_modal import update_task_modal, create_task_modal, task_modal_due_date_selector, task_modal_assignee_selector, task_modal_status_selector
from .create_project import create_project
from .join_project import join_project

def register(app):
    # Login
    app.action("login_button")(login_button)

    # Home main buttons
    app.action("create_project")(create_project)
    app.action("join_project")(join_project)
    app.action("refresh_home")(refresh_home)

    # Project filter buttons
    app.action("home_personal_project")(home_personal_project)
    app.action(re.compile("home_project-(.+)"))(home_project)

    # Project specific buttons
    app.action("create_task")(create_task_modal)
    app.action("search_tasks")(search_tasks)

    # Task Status filter buttons
    app.action(re.compile("home_task_status-(.+)"))(home_task_status)

    # Home task actions
    app.action(re.compile("update_task_modal-(.+)"))(update_task_modal)
    app.action(re.compile("delete_task_modal-(.+)"))(delete_task_action)

    # Task modal
    app.action("task_modal_assignee_selector")(task_modal_assignee_selector)
    app.action("task_modal_due_date_selector")(task_modal_due_date_selector)
    app.action("task_modal_status_selector")(task_modal_status_selector)

    # Invite members modal
    app.action(re.compile("developers"))(task_modal_assignee_selector)
    app.action(re.compile("qas"))(task_modal_assignee_selector)

    # Roll Off members modal
    app.action("members")(task_modal_assignee_selector)

    # Search Task
    app.action("min_due_date")(task_modal_due_date_selector)
    app.action("max_due_date")(task_modal_due_date_selector)
    app.action("min_created_date")(task_modal_due_date_selector)
    app.action("min_created_date")(task_modal_due_date_selector)
    app.action(re.compile("task_detail_modal-(.+)"))(task_detail_modal)

    # Misc
    app.action(re.compile("view_task_from_message"))(task_details_from_message)