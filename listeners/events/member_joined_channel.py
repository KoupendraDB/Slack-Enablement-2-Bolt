from services.backend.external import get_project_by_channel, get_project_members

def member_joined_channel(event, client, logger):
    from app import bot_info
    try:
        if event.get('inviter', '') != bot_info['user_id']:
            result = get_project_by_channel(event['channel'])
            project = result.get('project')
            if project:
                members = get_project_members(project['_id']).get('members')
                if event['user'] not in [user['username'] for user in members]:
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