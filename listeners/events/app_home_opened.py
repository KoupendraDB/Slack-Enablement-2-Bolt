from .helpers import handle_home_view

def app_home_opened(client, event, logger, body):
    try:
        team = body['team_id']
        user = event['user']
        if event['tab'] == 'home':
            handle_home_view(client, team, user)
    except Exception as e:
        logger.error(f"Error in app_home_opened: {e}")