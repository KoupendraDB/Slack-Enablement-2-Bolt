from ..events.helpers import handle_home_view

def home_task_status(ack, action, context, client):
    team = context['team_id']
    user = context['user_id']
    ack()
    handle_home_view(client, team, user, action['value'])

