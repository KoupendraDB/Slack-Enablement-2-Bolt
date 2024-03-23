from .helpers import handle_home_view

def app_home_opened(client, event, logger):
    try:
        team = event['view']['app_installed_team_id']
        user = event['user']
        handle_home_view(client, team, user)
    except Exception as e:
        print(e)
        logger.error(f"Error in app_home_opened: {e}")