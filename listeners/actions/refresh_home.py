from ..events.helpers import handle_home_view

def refresh_home(context, client, ack):
    ack()
    handle_home_view(client, context['team_id'], context['user_id'])