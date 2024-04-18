from services.backend.projects import get_project_from_channel
from services.backend.users import get_users

def get_option_groups(project):
    members = project['qas'] + project['developers']
    users_result = get_users({'username': {'$in': members}})
    users = users_result.get('users', [])
    names_of_users = {}
    for user in users:
        names_of_users[user['username']] = user['name']

    option_groups = []

    option_groups.append({
        "label": {
            "type": "plain_text",
            "text": "Developers"
        },
        "options": [
            {
                "text": {
                    "type": "plain_text",
                    "text": names_of_users[dev]
                },
                "value": dev
            } for dev in project.get('developers', [])
        ]
    })

    option_groups.append({
        "label": {
            "type": "plain_text",
            "text": "QAs"
        },
        "options": [
            {
                "text": {
                    "type": "plain_text",
                    "text": names_of_users[qa]
                },
                "value": qa
            } for qa in project.get('qas', [])
        ]
    })

    return [group for group in option_groups if len(group['options']) > 0]

def get_roll_off_modal(project):
    option_groups = get_option_groups(project)
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
        "callback_id": f"submit_roll_off-{project['_id']}",
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
            modal = get_roll_off_modal(project)
            
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