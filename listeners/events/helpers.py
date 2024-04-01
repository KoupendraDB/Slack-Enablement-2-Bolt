from services.backend.tasks import get_tasks
from datetime import date

tasks_statuses = ['Ready', 'In-Progress', 'Code Review', 'Deployed', 'QA', 'Rejected', 'Blocked', 'Accepted', 'Cancelled']

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
    elements = [
        {
            "type": "users_select",
            "placeholder": {
                "type": "plain_text",
                "text": "Assignee",
            },
            "initial_user": user,
            "action_id": f"assignee_selector-{user_task['_id']}"
        },
        {
            "type": "static_select",
            "placeholder": {
                "type": "plain_text",
                "text": "Status",
            },
            "options": get_task_status_options(),
            "initial_option": {
                "text": {
                    "type": "plain_text",
                    "text": user_task['status'],
                },
                "value": user_task['status']
            },
            "action_id": f"task_status_selector-{user_task['_id']}"
        },
        {
            "type": "datepicker",
            "initial_date": f"{user_task['eta_done'].split('T')[0]}",
            "placeholder": {
                "type": "plain_text",
                "text": "To be done by",
            },
            "action_id": f"task_eta_selector-{user_task['_id']}"
        }
    ]
    if user == user_task['created_by']:
        elements.append({
            "type": "button",
            "style": "danger",
            "text": {
                "type": "plain_text",
                "text": "Delete :walking:",
                "emoji": True
            },
            "value": "delete",
            "action_id": f"delete_task-{user_task['_id']}"
        })
    return elements

def generate_task_block(user_task, user):
    task = [
        {
            "type": "section",
            "block_id": f"task-{user_task['_id']}",
            "text": {
                "type": "mrkdwn",
                "text": f"*{user_task['title']}*"
            }
        },
        {
			"type": "actions",
			"elements": [{
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": "View details",
                    "emoji": True
                },
                "value": "details",
                "action_id": f"task_details-{user_task['_id']}"
            }]
		},
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

def generate_status_buttons(tasks, selected_status):
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
                "value": f"{status}",
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

def handle_home_view(client, team, user, selected_status = None):
    tasks_response = get_tasks(team, user)
    if tasks_response.get('success', False):
        status_buttons = generate_status_buttons(tasks_response['tasks'], selected_status)
        task_blocks = generate_tasks_blocks(tasks_response['tasks'], user, selected_status)
        blocks = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*{len(tasks_response['tasks'])} task(s) assigned to you*"
                },
                "accessory": {
                    "type": "button",
                    "style": "primary",
                    "text": {
                        "type": "plain_text",
                        "text": "Refresh :arrows_clockwise:",
                        "emoji": True
                    },
                    "value": "refresh",
                    "action_id": "refresh_home"
                }
            },
            {
                "type": "divider"
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
                            },
                            {
                                "type": "button",
                                "text": {
                                "type": "plain_text",
                                "text": "Register now"
                                },
                                "value": "register",
                                "action_id": "register_button"
                            }
                        ]
                    }
                ]
            }
        )