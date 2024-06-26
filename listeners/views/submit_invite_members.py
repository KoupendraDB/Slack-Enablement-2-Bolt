from .payload_helper import invite_members_from_payload
from services.backend.external import create_project_invite

def submit_invite_members(ack, payload, body, client, context):
    ack()
    project_id = payload['callback_id'].replace('submit_invite_members', '').replace('-', '')
    members = invite_members_from_payload(body['view']['state']['values'])
    if len(members) == 0:
        return
    result = create_project_invite(context['team_id'], context['user_id'], project_id, members)
    codes = result.get('invitation_codes')
    if not codes:
        return
    for member in members:
        client.chat_postMessage(
            channel = member,
            text=f"<@{context['user_id']}> has invited you to join a project!",
            blocks = [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"<@{context['user_id']}> has invited you to join a project!\n\nClick on *Join a Project* button and enter the following code: `{codes['invitations.' + member]}`"
                    },
                },
                {
                    "type": "actions",
                    "elements": [
                        {
                            "type": "button",
                            "style": "primary",
                            "text": {
                                "type": "plain_text",
                                "text": "Join a Project :technologist:",
                                "emoji": True
                            },
                            "action_id": "join_project",
                        }
                    ]
                }
            ]
        )