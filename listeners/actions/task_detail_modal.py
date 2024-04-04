from datetime import date
from services.backend.tasks import get_task
from .task_details import get_task_details

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
    result = get_task(task_id, team, user)
    if result.get('success', False):
        ack()
        client.views_push(
            trigger_id = trigger_id,
            view = create_task_detail_modal(result['task'])
        )
    