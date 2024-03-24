from ..events.helpers import handle_home_view
from services.backend.tasks import update_task

def task_eta_selector(ack, payload, context, client):
    team = context['team_id']
    user = context['user_id']
    eta_date = payload['selected_date']
    task_id = payload['action_id'].replace('task_eta_selector-', '')
    result = update_task(task_id, team, user, {'eta_done': f"{eta_date}"})
    if result.get('success', False):
        ack()
        handle_home_view(client, team, user)
    else:
        ack(
            response_action = 'errors',
            errors = {
                payload['block_id']: result.get('message', 'Invalid operation!')
            }
        )
    
