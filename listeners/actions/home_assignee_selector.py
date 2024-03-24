from ..events.helpers import handle_home_view
from services.backend.tasks import update_task

def home_assignee_selector(ack, payload, context, client):
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
    else:
        ack(
            response_action = 'errors',
            errors = {
                payload['block_id']: result.get('message', 'Invalid assignee!')
            }
        )
    
