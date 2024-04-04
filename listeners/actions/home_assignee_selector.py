from ..events.helpers import handle_home_view
from services.backend.tasks import update_task

def home_assignee_selector(ack, payload, context, client, say):
    team = context['team_id']
    user = payload['initial_user']
    new_assignee = payload['selected_user']
    if user == new_assignee:
        ack()
        return
    task_id = payload['action_id'].replace('assignee_selector-', '')
    result = update_task(task_id, team, user, {'assignee': f"{new_assignee}"})
    if result.get('success', False):
        ack()
        handle_home_view(client, team, user)
        say(
            channel=new_assignee,
            text = f"<@{user}> has assigned you a task!",
            blocks = [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"<@{user}> has assigned you a task!"
                    },
                    "accessory": {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "View :thinking_face:",
                            "emoji": True
                        },
                        "value": task_id,
                        "action_id": f"view_task_from_message-{task_id}"
                    }
                }
            ]
        )
    else:
        ack(
            response_action = 'errors',
            errors = {
                payload['block_id']: result.get('message', 'Invalid assignee!')
            }
        )
    
