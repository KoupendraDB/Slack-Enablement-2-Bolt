from services.backend.tasks import get_tasks

def get_task_status_options():
    tasks_statuses = ['Ready', 'In-Progress', 'Code Review', 'Deployed', 'QA', 'Rejected', 'Blocked', 'Accepted', 'Cancelled']
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
    
def generate_tasks_blocks(user_tasks, user):
    tasks = []
    for user_task in user_tasks:
        task = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*{user_task['title']}*"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "plain_text",
                    "text": f"{user_task.get('description', 'null')}",
                    "emoji": True
                }
            },
            {
                "type": "actions",
                "elements": [
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
            },
            {
                "type": "divider"
            }
        ]
        tasks.extend(task)
    return tasks

def handle_home_view(client, team, user):
    tasks_response = get_tasks(team, user)
    if tasks_response.get('success', False):
        task_blocks = generate_tasks_blocks(tasks_response['tasks'], user)
        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"{len(tasks_response['tasks'])} ticket(s) assigned to you",
                }
            },
            {
                "type": "divider"
            }
        ]
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