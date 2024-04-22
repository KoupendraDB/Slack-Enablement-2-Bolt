from services.backend.external import roll_off_members, get_project
from .payload_helper import roll_off_members_from_payload

def submit_roll_off(ack, context, payload, body, client):
    project_id = payload['callback_id'].replace('submit_roll_off-', '')
    members = roll_off_members_from_payload(body['view']['state']['values'])
    project_result = get_project(context['team_id'], context['user_id'], project_id)
    project = project_result['project']
    ack()
    roll_off_result = roll_off_members(context['team_id'], context['user_id'], project_id, members)
    if roll_off_result.get('success', False):
        for member in members:
            client.conversations_kick(
                channel = project['channel_id'],
                user = member
            )
            client.chat_postMessage(
                channel = member,
                text = f"You have been rolled off from `{project['name']}`"
            )
    else:
        client.chat_postEphemeral(
            channel = project['channel_id'],
            user = context['user_id'],
            text = "Session expired! Please log in again"
        )