from services.backend.external import get_user_project_tasks, get_user_personal_tasks, get_user_projects
from services.backend.roles import fetch_user_role
from datetime import date, datetime
from json import loads

tasks_statuses = ['To-Do', 'In-Progress', 'In-QA', 'Done']

def get_task_status_options():
    blocks = []
    for status in tasks_statuses:
        blocks.append({
            "text": {
                "type": "plain_text",
                "text": status,
            },
            "value": status
        })
    return blocks

def get_action_elements(user, user_task):
    elements = [{
        "type": "button",
        "text": {
            "type": "plain_text",
            "text": "Update :pencil2:",
            "emoji": True
        },
        "value": user_task['_id'],
        "action_id": f"update_task_modal-{user_task['_id']}"
    }]
    if user == user_task['created_by']:
        elements.append({
            "type": "button",
            "style": "danger",
            "text": {
                "type": "plain_text",
                "text": "Delete :walking:",
                "emoji": True
            },
            "value": user_task['_id'],
            "action_id": f"delete_task_modal-{user_task['_id']}"
        })
    return elements

def get_task_details(user_task):
    last_modified_at = datetime.fromisoformat(user_task['last_modified_at'])
    created_at = datetime.fromisoformat(user_task['created_at'])
    due_date = datetime.fromisoformat(user_task['eta_done'])
    details = [{
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": f"_Due on {due_date.strftime('%m/%d/%Y')}_",\
        }
	}]
    if user_task.get('project', False):
        details.extend([
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"Last modified by <@{user_task['last_modified_by']}>"
                }
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "plain_text",
                        "text": f"on {last_modified_at.strftime('%m/%d/%Y at %H:%M:%S')}",
                    }
                ]
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"Created by <@{user_task['created_by']}>"
                }
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "plain_text",
                        "text": f"on {created_at.strftime('%m/%d/%Y at %H:%M:%S')}",
                    }
                ]
            }
        ])
    if user_task.get('description_type', '') == 'mrkdwn':
        description = {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": user_task['description']
                        }
                    }
    else:
        description = loads(user_task['description'])
    task_details = [description] + details
    return task_details

def generate_task_block(user_task, user):
    task_details = get_task_details(user_task)
    task = [
        {
            "type": "section",
            "block_id": f"task-{user_task['_id']}",
            "text": {
                "type": "mrkdwn",
                "text": f"*{user_task['title']}*"
            }
        },
        *task_details,
        {
            "type": "actions",
            "elements": get_action_elements(user, user_task)
        },
        {
            "type": "divider"
        }
    ]
    return task

def generate_tasks_blocks(user_tasks, user, selected_status):
    tasks_by_status = {}
    tasks = []
    for task in user_tasks: 
        if selected_status:
            if (task['status'] == selected_status):
                tasks.append(task)
        else:
            tasks.append(task)
    for user_task in tasks:
        if user_task['status'] not in tasks_by_status:
            tasks_by_status[user_task['status']] = []
        tasks_by_status[user_task['status']].append(user_task)
    
    blocks = []
    for status in tasks_statuses:
        if status in tasks_by_status:
            if not selected_status:
                blocks.extend([
                    {
                        "type": "divider"
                    },
                    {
                        "type": "header",
                        "text": {
                            "type": "plain_text",
                            "text": status,
                        }
                    },
                    {
                        "type": "divider"
                    }
                ])
            sorted_tasks = sorted(tasks_by_status[status], key = lambda t: date.fromisoformat(t['eta_done']))
            for status_task in sorted_tasks:
                task = generate_task_block(status_task, user)
                blocks.extend(task)
    return blocks

def generate_status_buttons(tasks, selected_project, selected_status):
    status_count = {}
    for task in tasks:
        status_count[task['status']] = status_count.get(task['status'], 0) + 1

    elements = []
    for status in tasks_statuses:
        count = status_count.get(status, 0)
        if count > 0:
            button = {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": f"{status} ({status_count.get(status, 0)})"
                },
                "value": f"{selected_project if selected_project else ''}:{status}",
                "action_id": f"home_task_status-{status}",
            }
            if status == selected_status:
                button['style'] = 'primary'
            elements.append(button)

    actions = {
        "type": "actions",
        "elements": elements
    }

    return actions

def generate_projects_buttons(projects, selected_project):
    elements = [{
        "type": "button",
        "text": {
            "type": "plain_text",
            "text": f"Personal Tasks"
        },
        "action_id": "home_personal_project",
    }]

    for project in projects:
        button = {
            "type": "button",
            "text": {
                "type": "plain_text",
                "text": f"{project['name']}"
            },
            "value": f"{project['_id']}",
            "action_id": f"home_project-{project['_id']}",
        }
        if project['_id'] == selected_project:
            button['style'] = 'primary'
        elements.append(button)

    if not selected_project:
        elements[0]['style'] = 'primary'

    actions = {
        "type": "actions",
        "elements": elements
    }
    return actions

def handle_home_view(client, team, user, selected_project = None, selected_status = None):
    tasks_response = get_user_project_tasks(team, user, selected_project) if selected_project else get_user_personal_tasks(team, user)
    project_response = get_user_projects(team, user)
    if tasks_response.get('success', False):
        status_buttons = generate_status_buttons(tasks_response['tasks'], selected_project, selected_status)
        projects_buttons = generate_projects_buttons(project_response['projects'], selected_project)
        task_blocks = generate_tasks_blocks(tasks_response['tasks'], user, selected_status)
        user_role = fetch_user_role(team, user)
        main_action_buttons = [
            {
                "type": "button",
                "style": "primary",
                "text": {
                    "type": "plain_text",
                    "text": "Join a Project :technologist:",
                    "emoji": True
                },
                "action_id": "join_project",
            },
            {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": "Refresh :arrows_clockwise:",
                    "emoji": True
                },
                "action_id": "refresh_home"
            }
        ]

        create_task_button = {
            "type": "button",
            "style": "primary",
            "text": {
                "type": "plain_text",
                "text": "Create a task :heavy_plus_sign:",
                "emoji": True
            },
            "action_id": "create_task",
        }
        if selected_project:
            create_task_button['value'] = selected_project
            main_action_buttons[1]['value'] = selected_project

        project_specific_buttons = [create_task_button]

        if user_role == 'admin':
            main_action_buttons.insert(0, {
                "type": "button",
                "style": "primary",
                "text": {
                    "type": "plain_text",
                    "text": "Create a Project :notebook:",
                    "emoji": True
                },
                "action_id": "create_project",
            })
        
        if (user_role in ['admin', 'project_manager']) and selected_project:
            project_specific_buttons.append({
            "type": "button",
            "text": {
                "type": "plain_text",
                "text": "Search tasks :mag:",
                "emoji": True
            },
            "value": selected_project,
            "action_id": "search_tasks",
        })

        blocks = [
            {
                "type": "actions",
                "elements": main_action_buttons
            },
            {
                "type": "divider"
            },
            projects_buttons,
            {
                "type": "divider"
            },
            {
                "type": "actions",
                "elements": project_specific_buttons
            },
            {
                "type": "divider"
            },
            {
            "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"{len(tasks_response['tasks'])} task(s) assigned to you"
                }
            }
        ]
        if len(status_buttons['elements']) > 0:
            blocks.extend([
                status_buttons,
                {
                    "type": "divider"
                }
            ])
        blocks.extend(task_blocks)
        client.views_publish(
            user_id=user,
            view={
                "type": "home",
                "blocks": blocks
            }
        )
    else:
        client.views_publish(
            user_id=user,
            view={
                "type": "home",
                "blocks": [
                    {
                        "type": "header",
                        "text": {
                            "type": "plain_text",
                            "text": "You have to log in to use the app!"
                        }
                    },
                    {
                        "type": "divider"
                    },
                    {
                        "type": "actions",
                        "elements": [
                            {
                                "type": "button",
                                "style": "primary",
                                "text": {
                                    "type": "plain_text",
                                    "text": "Log In",
                                },
                                "value": "login",
                                "action_id": "login_button"
                            }
                        ]
                    }
                ]
            }
        )