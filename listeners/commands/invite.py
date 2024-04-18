from services.backend.projects import get_project_from_channel

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
        projects_result = get_project_from_channel(command['channel_id'])
        projects = projects_result['projects']
        if len(projects) > 0:
            project = projects[0]
            if command['user_id'] not in [project['project_manager'], project['admin']]:
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