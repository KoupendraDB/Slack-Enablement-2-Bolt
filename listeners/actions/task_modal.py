from services.backend.tasks import get_task
from ..events.helpers import get_task_status_options
from datetime import date
import json

def get_update_task_modal(user, user_task, task_id):
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
    if user_task.get('project', False):
        action_elements.insert(0, {
            "type": "users_select",
            "placeholder": {
                "type": "plain_text",
                "text": "Select an user",
            },
            "initial_user": user,
            "action_id": "task_modal_assignee_selector"
        })
    modal['blocks'].append(action_elements)
    return modal

def get_create_task_modal(user, project = None, description = {'type': 'rich_text', 'elements': []}):
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
    if project:
        action_elements.insert(0, {
            "type": "users_select",
            "placeholder": {
                "type": "plain_text",
                "text": "Select an user",
            },
            "initial_user": user,
            "action_id": "task_modal_assignee_selector"
        })
    modal['blocks'].append(action_elements)
    return modal

def update_task_modal(ack, context, action, client, body):
    team = context['team_id']
    user = context['user_id']
    task_id = action['value']
    result = get_task(task_id, team, user)
    if result.get('success', False):
        modal = get_update_task_modal(user, result['task'], task_id)
        client.views_open(
            trigger_id = body["trigger_id"],
            view = modal
        )
    ack()


def create_task_modal(ack, body, client, logger, context):
    try:
        ack()
        user = context['user_id']
        modal = get_create_task_modal(user)
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