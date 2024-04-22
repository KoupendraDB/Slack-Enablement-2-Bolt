from services.backend.external import get_task, get_project, get_project_members
from ..events.helpers import get_task_status_options
from datetime import date
import json

def get_assignee_selector_options(project_id, initial_user = None):
    users = {}
    get_users_result = get_project_members(project_id)
    project_users = get_users_result['members']

    option_groups = [
        {
            "label": {
                "type": "plain_text",
                "text": f"{role_name}"
            },
            "options": []
        } for role_name in ['Project Manager', 'Developers', 'QAs', 'Admin']
    ]

    for user in project_users:
        users[user['username']] = user['name']
        option = {
            "text": {
                "type": "plain_text",
                "text": user['name']
            },
            "value": user['username']
        }
        if user['role'] == 'project_manager':
            option_groups[0]['options'].append(option)
        elif user['role'] == 'developer':
            option_groups[1]['options'].append(option)
        elif user['role'] == 'qa':
            option_groups[2]['options'].append(option)
        elif user['role'] == 'admin':
            option_groups[3]['options'].append(option)

    filtered_groups = list(filter(lambda x: len(x['options']) > 0, option_groups))
    
    if initial_user:
        return filtered_groups, {
            "text": {
                "type": "plain_text",
                "text": users[initial_user]
            },
            "value": initial_user
        }
    return filtered_groups, None


def get_update_task_modal(context, user_task, task_id):
    user = context['user_id']
    if user_task.get('description_type', '') == 'mrkdwn':
        description = {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": user_task['description']
                        }
                    }
    else:
        description = json.loads(user_task['description'])
    modal = {
        "title": {
            "type": "plain_text",
            "text": "Update Task"
        },
        "submit": {
            "type": "plain_text",
            "text": "Submit",
        },
        "callback_id": f"update_task-{task_id}",
        "blocks": [
            {
                "type": "input",
                "element": {
                    "type": "plain_text_input",
                    "action_id": "task_title_input",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Task title"
                    },
                    "initial_value": user_task['title']
                },
                "block_id": "task_title_block",
                "label": {
                    "type": "plain_text",
                    "text": "Title"
                }
            },
            {
                "type": "input",
                "block_id": "task_description_block",
                "element": {
                    "type": "rich_text_input",
                    "action_id": "task_description_input",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Task Description"
                    },
                    "initial_value": description
                },
                "label": {
                    "type": "plain_text",
                    "text": "Description"
                }
            },
        ],
        "type": "modal"
    }
    action_elements = {
        "type": "actions",
        "block_id": "selectors",
        "elements": [
            {
                "type": "static_select",
                "placeholder": {
                    "type": "plain_text",
                    "text": "Select status",
                },
                "options": get_task_status_options(),
                "initial_option": {
                    "text": {
                        "type": "plain_text",
                        "text": user_task['status'],
                    },
                    "value": user_task['status']
                },
                "action_id": "task_modal_status_selector"
            },
            {
                "type": "datepicker",
                "initial_date": user_task['eta_done'],
                "placeholder": {
                    "type": "plain_text",
                    "text": "Select a due date",
                },
                "action_id": "task_modal_due_date_selector"
            }
        ]
    }
    project_id = user_task.get('project', None)
    if project_id:
        option_groups, initial_option = get_assignee_selector_options(project_id, user)
        action_elements['elements'].insert(0, {
            "type": "static_select",
            "action_id": f"task_modal_assignee_selector",
            "initial_option": initial_option,
            "option_groups": option_groups
        })
    modal['blocks'].append(action_elements)
    return modal

def get_create_task_modal(context, project_id = None, description = {'type': 'rich_text', 'elements': []}, project = None):
    team = context['team_id']
    user = context['user_id']
    modal = {
        "title": {
            "type": "plain_text",
            "text": "Create Task"
        },
        "submit": {
            "type": "plain_text",
            "text": "Create",
        },
        "callback_id": "submit_new_task",
        "blocks": [
            {
                "type": "input",
                "element": {
                    "type": "plain_text_input",
                    "action_id": "task_title_input",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Task title"
                    }
                },
                "block_id": "task_title_block",
                "label": {
                    "type": "plain_text",
                    "text": "Title"
                }
            },
            {
                "type": "input",
                "block_id": "task_description_block",
                "element": {
                    "type": "rich_text_input",
                    "action_id": "task_description_input",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Task Description"
                    },
                    "initial_value": description
                },
                "label": {
                    "type": "plain_text",
                    "text": "Description"
                }
            }
        ],
        "type": "modal"
    }
    action_elements = {
        "type": "actions",
        "block_id": "selectors",
        "elements": [
            {
                "type": "static_select",
                "placeholder": {
                    "type": "plain_text",
                    "text": "Select status",
                },
                "options": get_task_status_options(),
                "initial_option": {
                    "text": {
                        "type": "plain_text",
                        "text": "To-Do",
                    },
                    "value": "To-Do"
                },
                "action_id": "task_modal_status_selector"
            },
            {
                "type": "datepicker",
                "initial_date": date.today().isoformat(),
                "placeholder": {
                    "type": "plain_text",
                    "text": "Select a due date",
                },
                "action_id": "task_modal_due_date_selector"
            }
        ]
    }
    if project_id and not project:
        project_result = get_project(team, user, project_id)
        project = project_result.get('project')
    if project:
        option_groups, initial_option = get_assignee_selector_options(project_id, user)
        modal['blocks'].insert(0, {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*Project:* {project['name']}"
            }
        })
        action_elements['elements'].insert(0, {
            "type": "static_select",
            "action_id": f"task_modal_assignee_selector",
            "initial_option": initial_option,
            "option_groups": option_groups
        })
        modal['callback_id'] += f'-{project_id}'
    modal['blocks'].append(action_elements)
    return modal

def update_task_modal(ack, context, action, client, body):
    ack()
    team = context['team_id']
    user = context['user_id']
    task_id = action['value']
    result = get_task(team, user, task_id)
    if result.get('success', False):
        modal = get_update_task_modal(context, result['task'], task_id)
        client.views_open(
            trigger_id = body["trigger_id"],
            view = modal
        )


def create_task_modal(ack, body, client, logger, context, action):
    try:
        ack()
        modal = get_create_task_modal(context, action.get('value', None))
        client.views_open(
            trigger_id = body["trigger_id"],
            view = modal
        )
    except Exception as e:
        logger.error(f"Error in create_task: {e}")


def task_modal_assignee_selector(ack):
    ack()

def task_modal_status_selector(ack):
    ack()

def task_modal_due_date_selector(ack):
    ack()