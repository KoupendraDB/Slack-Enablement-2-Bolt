from ..events.helpers import handle_home_view

def home_task_status(ack, action, context, client):
    team = context['team_id']
    user = context['user_id']
    ack()
    project, status = action['value'].split(':')
    handle_home_view(client, team, user, project, status)
