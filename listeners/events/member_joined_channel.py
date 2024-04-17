from services.backend.projects import get_project_from_channel

def member_joined_channel(event, client, logger):
    from app import bot_info
    try:
        if event['inviter'] != bot_info['user_id']:
            project_search_result = get_project_from_channel(event['channel'])
            projects = project_search_result['projects']
            if len(projects) > 0:
                project = projects[0]
                members = project['qas'] + project['developers'] + [project['admin'], project['project_manager']]
                if event['user'] not in members:
                    client.conversations_kick(
                        channel = event['channel'],
                        user = event['user']
                    )
                    client.chat_postEphemeral(
                        channel = event['channel'],
                        user = event['inviter'],
                        text = f"<@{event['user']}> is not part of the project and hence removed from channel!"
                    )
    except Exception as e:
        logger.error(f"Error in member_joined_channel: {e}")