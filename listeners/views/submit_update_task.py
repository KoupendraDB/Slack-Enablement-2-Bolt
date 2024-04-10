from .payload_helper import task_form_from_payload
from ..events.helpers import handle_home_view
from services.backend.tasks import update_task

def submit_update_task(ack, logger, body, context, client, payload, say):
    try:
        form = task_form_from_payload(body['view']['state']['values'], context['user_id'])
        task_id = payload['callback_id'].replace('update_task-', '')
        result = update_task(task_id, context['team_id'], context['user_id'], form)
        if result.get('success', False):
            ack()
            handle_home_view(client, context['team_id'], context['user_id'])
            if context['user_id'] != form['assignee']:
                say(
                    channel=form['assignee'],
                    text = f"<@{context['user_id']}> has assigned you a task: {form['title']}! ",
                    blocks = [
                        {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": f"<@{context['user_id']}> has assigned you a task!"
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
                    payload['title']: result.get('message', 'Check inputs!')
                }
            )
    except Exception as e:
        logger.error(f'Error in submit_update_task: {e}')