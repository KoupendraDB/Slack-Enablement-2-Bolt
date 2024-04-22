from datetime import date, datetime
from services.backend.external import get_task
from json import loads

def get_task_details(user_task):
    last_modified_at = datetime.fromisoformat(user_task['last_modified_at'])
    created_at = datetime.fromisoformat(user_task['created_at'])
    details = [
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
    ]
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

def create_task_detail_modal(task):
    blocks = [
        {
            "type": "divider"
        },
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": f"{task['title']}",
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*Assignee:* <@{task['assignee']}>",
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*Status:* {task['status']}",
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*Due date:* {date.fromisoformat(task['eta_done']).strftime('%m/%d/%Y')}",
            }
        },
        {
            "type": "divider"
        }
    ]
    blocks.extend(get_task_details(task))
    view = {
        "type": "modal",
        "title": {
            "type": "plain_text",
            "text": "Task"
        },
        "close": {
            "type": "plain_text",
            "text": "Back"
        },
        "blocks": blocks
    }
    return view

def task_detail_modal(ack, body, client, context, action):
    team = context['team_id']
    user = context['user_id']
    task_id = action['value']
    trigger_id = body['trigger_id']
    result = get_task(team, user, task_id)
    if result.get('success', False):
        ack()
        client.views_push(
            trigger_id = trigger_id,
            view = create_task_detail_modal(result['task'])
        )
    