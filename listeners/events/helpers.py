from services.backend.tasks import get_tasks

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
                        "action_id": "assignee_selector"
                    },
                    {
                        "type": "static_select",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Status",
                        },
                        "options": [
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "Ready",
                                },
                                "value": "ready"
                            },
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "In-Progress",
                                },
                                "value": "progress"
                            },
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "QA",
                                },
                                "value": "qa"
                            }
                        ],
                        "initial_option": {
                            "text": {
                                "type": "plain_text",
                                "text": "Ready",
                            },
                            "value": "ready"
                        },
                        "action_id": "static_select-action"
                    },
                    {
                        "type": "datepicker",
                        "initial_date": f"{user_task['eta_done'].split('T')[0]}",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "To be done by",
                        },
                        "action_id": "datepicker-action"
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
                            }
                        ]
                    }
                ]
            }
        )