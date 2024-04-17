from .payload_helper import invite_members_from_payload
from services.backend.project_invites import create_project_invite_code

def submit_invite_members(ack, payload, body, client, context):
    ack()
    project_id = payload['callback_id'].replace('submit_invite_members', '').replace('-', '')
    members = invite_members_from_payload(body['view']['state']['values'])
    if len(members) == 0:
        return
    token = create_project_invite_code(project_id, members)
    for member in members:
        client.chat_postMessage(
            channel = member,
            text=f"<@{context['user_id']}> has invited you to join a project!",
            blocks = [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"<@{context['user_id']}> has invited you to join a project!\n\nClick on *Join a Project* button and enter the following code: `{token}`"
                    }
                }
            ]
        )