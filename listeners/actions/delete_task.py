from ..events.helpers import handle_home_view
from services.backend.tasks import delete_task

def delete_task_action(ack, context, payload, client):
    task_id = payload['action_id'].replace('delete_task-', '')
    result = delete_task(task_id, context['team_id'], context['user_id'])
    if result.get('success', False):
        ack()
        handle_home_view(client, context['team_id'], context['user_id'])
    else:
        ack(
            response_action = 'errors',
            errors = {
                payload['block_id']: result.get('message', 'Invalid operation!')
            }
        )