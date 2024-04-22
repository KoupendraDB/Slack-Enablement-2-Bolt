from services.backend.external import get_project_by_channel, get_project_members
from services.backend.roles import fetch_user_role

def get_option_groups(project_id):
    get_users_result = get_project_members(project_id)
    project_users = get_users_result['members']

    option_groups = [
        {
            "label": {
                "type": "plain_text",
                "text": f"{role_name}"
            },
            "options": []
        } for role_name in ['Developers', 'QAs']
    ]

    for user in project_users:
        option = {
            "text": {
                "type": "plain_text",
                "text": user['name']
            },
            "value": user['username']
        }
        if user['role'] == 'developer':
            option_groups[0]['options'].append(option)
        elif user['role'] == 'qa':
            option_groups[1]['options'].append(option)

    filtered_groups = list(filter(lambda x: len(x['options']) > 0, option_groups))
    return filtered_groups

def get_roll_off_modal(project_id):
    option_groups = get_option_groups(project_id)
    if len(option_groups) == 0:
        return None

    return {
        "title": {
            "type": "plain_text",
            "text": "Roll Off members"
        },
        "submit": {
            "type": "plain_text",
            "text": "Roll Off",
        },
        "callback_id": f"submit_roll_off-{project_id}",
        "blocks": [
            {
                "type": "section",
                "block_id": "members",
                "text": {
                    "type": "mrkdwn",
                    "text": "Select Members to Roll Off"
                },
                "accessory": {
                    "action_id": "members",
                    "type": "multi_static_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Select Members"
                    },
                    "option_groups": option_groups
                }
            }
        ],
        "type": "modal"
    }


def command_roll_off(ack, logger, command, client, body):
    try:
        result = get_project_by_channel(command['channel_id'])
        project = result.get('project')
        ack()
        if project:
            role = fetch_user_role(command['team_id'], command['user_id'])
            if role not in ['project_manager', 'admin']:
                client.chat_postEphemeral(
                    channel=command['channel_id'],
                    user=command['user_id'],
                    text = "You don't have permission to invite!"
                )
                return
            modal = get_roll_off_modal(project['_id'])
            
            if modal:
                client.views_open(
                    trigger_id = body['trigger_id'],
                    view = modal
                )
            else:
                client.chat_postEphemeral(
                    channel=command['channel_id'],
                    user=command['user_id'],
                    text = "No developers or QAs in project!"
                )
        else:
            client.chat_postEphemeral(
                channel=command['channel_id'],
                user=command['user_id'],
                text = "Project isn't associated with the Task Manager app!"
            )
        ack()
    except Exception as e:
        logger.error(f"Error in command_roll_off: {e}")