from services.backend.external import accept_project_invite
from services.backend.roles import fetch_user_role


def submit_join_project(ack, body, context, client):
    invite_code = body['view']['state']['values']['invite_code']['invite_code']['value']
    result = accept_project_invite(context['team_id'], context['user_id'], invite_code)
    if result.get('success', False):
        ack()
        project = result.get('project')
        role = fetch_user_role(context['team_id'], context['user_id'])
        channel_id = project['channel_id']
        client.conversations_invite(channel = channel_id, users = [context['user_id']])
        client.chat_postMessage(
            channel = context['user_id'],
            text = f"You have successfully joined {project['name']}!"
        )
        client.chat_postMessage(
            channel = channel_id,
            text = f"<@{context['user_id']}> has joined the project as {'QA' if role == 'qa' else 'Developer'}"
        )
    else:
        ack(
            response_action = 'errors',
            errors = {
                'invite_code': result.get('Message', 'Unknown error!')
            }
        )