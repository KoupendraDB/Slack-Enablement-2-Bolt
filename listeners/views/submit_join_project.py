from services.backend.project_invites import get_project_id_from_invite_code
from services.backend.projects import get_project, update_project
from services.backend.roles import fetch_user_role


def submit_join_project(ack, body, context, client):
    invite_code = body['view']['state']['values']['invite_code']['invite_code']['value']
    project_id = get_project_id_from_invite_code(invite_code, context['user_id'])
    if project_id:
        project_result = get_project(context['team_id'], context['user_id'], project_id)
        if project_result.get('success', False):
            project = project_result['project']
            role = fetch_user_role(context['team_id'], context['user_id'])
            user_already_in_project = True
            role_category = 'developers'
            if role == 'qa':
                role_category = 'qas'
            user_already_in_project = context['user_id'] in project[role_category]
            if user_already_in_project:
                ack(
                    response_action = 'errors',
                    errors = {
                        'invite_code': 'You are already in project!'
                    }
                )
                return
            ack()
            update_project_result  = update_project(context['team_id'], context['user_id'], project_id, {'$addToSet': {role_category: context['user_id']}})
            if update_project_result.get('success', False):
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
                    'invite_code': 'Session expired! Please log in'
                }
            )
    else:
        ack(
            response_action = 'errors',
            errors = {
                'invite_code': 'Invalid invite code!'
            }
        )