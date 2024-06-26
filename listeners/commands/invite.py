from services.backend.external import get_project_by_channel
from services.backend.roles import fetch_user_role

def get_invite_member_modal(project_id):
    return {
        "title": {
            "type": "plain_text",
            "text": "Invite members"
        },
        "submit": {
            "type": "plain_text",
            "text": "Create",
        },
        "callback_id": f"submit_invite_members-{project_id}",
        "blocks": [
            {
                "type": "section",
                "block_id": "developers",
                "text": {
                    "type": "mrkdwn",
                    "text": "Select Developers to invite"
                },
                "accessory": {
                    "action_id": "developers",
                    "type": "multi_external_select",
                    "min_query_length": 2,
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Select Developers"
                    }
                }
            },
            {
                "type": "section",
                "block_id": "qas",
                "text": {
                    "type": "mrkdwn",
                    "text": "Select QAs to invite"
                },
                "accessory": {
                    "action_id": "qas",
                    "type": "multi_external_select",
                    "min_query_length": 2,
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Select QAs"
                    },
                }
            }
        ],
        "type": "modal"
    }

def command_invite_member(ack, body, logger, client, command):
    try:
        result = get_project_by_channel(command['channel_id'])
        project = result.get('project')
        if project:
            role = fetch_user_role(command['team_id'], command['user_id'])
            if role not in ['project_manager', 'admin']:
                client.chat_postEphemeral(
                    channel=command['channel_id'],
                    user=command['user_id'],
                    text = "You don't have permission to invite!"
                )
                ack()
                return
            modal = get_invite_member_modal(project['_id'])
            client.views_open(
                trigger_id = body['trigger_id'],
                view = modal
            )
        else:
            client.chat_postEphemeral(
                channel=command['channel_id'],
                user=command['user_id'],
                text = "Project isn't associated with the Task Manager app!"
            )
        ack()
    except Exception as e:
        logger.error(f"Error in command_invite_member: {e}")