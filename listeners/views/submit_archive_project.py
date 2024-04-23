from services.backend.external import archive_project, get_project

def submit_archive_project(ack, payload, context, client):
    ack()
    project_id = payload['callback_id'].replace('submit_archive_project-', '')
    archive_project_result = archive_project(context['team_id'], context['user_id'], project_id)
    if archive_project_result.get('success', False):
        get_project_result = get_project(context['team_id'], context['user_id'], project_id)
        if get_project_result.get('success', False):
            project = get_project_result['project']
            channel_id = project['channel_id']
            client.conversations_archive(channel = channel_id)
            client.chat_postMessage(
                channel = context['user_id'],
                text = f"{project['name']} has been archived successfully!"
            )
    else:
        client.chat_postMessage(
            channel = context['user_id'],
            text = f"Archiving {project['name']} failed!"
        )
