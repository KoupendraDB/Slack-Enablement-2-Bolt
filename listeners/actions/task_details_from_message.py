from services.backend.tasks import get_task
from .task_detail_modal import create_task_detail_modal


def task_details_from_message(ack, action, context, client, body):
    task_id = action['value']
    user = context['user_id']
    workspace = context['team_id']
    result = get_task(task_id, workspace, user)
    ack()
    if result.get('success', False):
        client.views_open(
            trigger_id = body['trigger_id'],
            view = create_task_detail_modal(result['task'])
        )
    else:
        client.chat_postEphemeral(
            channel=context['user_id'],
            user=context['user_id'],
            text = 'Session expired! Please log in from home'
        )