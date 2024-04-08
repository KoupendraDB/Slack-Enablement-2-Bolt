from ..events.helpers import handle_home_view

def home_project(ack, action, context, client):
    team = context['team_id']
    user = context['user_id']
    ack()
    project = action['value']
    handle_home_view(client, team, user, project)


def home_personal_project(ack, action, context, client):
    team = context['team_id']
    user = context['user_id']
    ack()
    handle_home_view(client, team, user)