from services.backend.projects import get_project_from_channel
from services.backend.users import get_users

def get_options(project, users):
    project_members = project['developers'] + project['qas']
    qa_group = {
        "label": {
            "type": "plain_text",
            "text": "QAs"
        },
        "options": []
    }
    dev_group = {
        "label": {
            "type": "plain_text",
            "text": "Developers"
        },
        "options": []
    }
    for user in users:
        if user['username'] in project_members:
            continue
        
        if user['role'] == 'qa':
            qa_group['options'].append({
                "text": {
                    "type": "plain_text",
                    "text": user['name']
                },
                "value": user['username']
            })
        elif user['role'] == 'developer':
            dev_group['options'].append({
                "text": {
                    "type": "plain_text",
                    "text": user['name']
                },
                "value": user['username']
            })
    
    option_groups = []
    if len(dev_group['options']):
        option_groups.append(dev_group)
    if len(qa_group['options']):
        option_groups.append(qa_group)
    return option_groups

def get_invite_member_modal(project, users):
    option_groups = get_options(project, users)
    if len(option_groups) == 0:
        return
    project_id = project['_id']
    modal = {
        "title": {
            "type": "plain_text",
            "text": "Invite a member"
        },
        "submit": {
            "type": "plain_text",
            "text": "Create",
        },
        "callback_id": f"submit_invite_member-{project_id}",
        "blocks": [
            {
                "type": "section",
                "block_id": "users",
                "text": {
                    "type": "mrkdwn",
                    "text": "Select users to invite"
                },
                "accessory": {
                    "action_id": "users",
                    "type": "multi_static_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Select users"
                    },
                    "option_groups": option_groups
                }
            }
        ],
        "type": "modal"
    }
    return modal

def command_invite_member(ack, body, logger, client, command):
    try:
        projects_result = get_project_from_channel(command['team_id'], command['user_id'], command['channel_id'])
        if projects_result.get('success', False):
            projects = projects_result['projects']
            if len(projects) > 0:
                project = projects[0]
                users_result = get_users({'$or': [
                    {'role': 'developer'},
                    {'role': 'qa'}
                ]})
                users = users_result.get('users', [])
                modal = get_invite_member_modal(project, users)
                if modal:
                    client.views_open(
                        trigger_id = body['trigger_id'],
                        view = modal
                    )
                else:
                    client.chat_postEphemeral(
                        channel=command['channel_id'],
                        user=command['user_id'],
                        text = "No users available!"
                    )
            else:
                client.chat_postEphemeral(
                    channel=command['channel_id'],
                    user=command['user_id'],
                    text = "Project isn't associated with the Task Manager app!"
                )
        else:
            client.chat_postEphemeral(
                channel=command['channel_id'],
                user=command['user_id'],
                text = "Session expired! Please login to the Task Manager app!"
            )
        ack()
    except Exception as e:
        logger.error(f"Error in command_invite_member: {e}")