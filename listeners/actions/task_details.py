from services.backend.tasks import get_task
from datetime import datetime
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

def get_updated_view(blocks, task_id, user_task):
    task_details = get_task_details(user_task)
    task_block_id = f"task-{task_id}"
    index = 0
    for i in range(len(blocks)):
        block = blocks[i]
        if block.get('block_id', '') == task_block_id:
            index = i + 1
            break
    return blocks[:index] + task_details + blocks[index + 1:]

def task_details(ack, client, payload, context, body):
    ack()
    team = context['team_id']
    user = context['user_id']
    task_id = payload['action_id'].replace('task_details-', '')
    result = get_task(task_id, team, user)
    if result.get('success', False):
        new_view = get_updated_view(body['view']['blocks'], task_id, result['task'])
        client.views_publish(
            user_id=user,
            view={
                "type": "home",
                "blocks": new_view
            }
        )
    ack()