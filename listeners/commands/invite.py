from services.backend.projects import get_project_from_channel
from services.backend.users import get_users

def get_options(project, users):
    project_members = project['developers'] + project['qas']
    qas = []
    devs = []
    for user in users:
        if user['username'] in project_members:
            continue
        
        if user['role'] == 'qa':
            qas.append({
                "text": {
                    "type": "plain_text",
                    "text": user['name']
                },
                "value": user['username']
            })
        elif user['role'] == 'developer':
            devs.append({
                "text": {
                    "type": "plain_text",
                    "text": user['name']
                },
                "value": user['username']
            })
    
    return devs, qas

def get_invite_member_modal(project, users):
    dev_options, qa_options = get_options(project, users)
    if len(dev_options) == 0 and len(qa_options) == 0:
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
        "callback_id": f"submit_invite_members-{project_id}",
        "blocks": [],
        "type": "modal"
    }
    if len(dev_options) > 0:
        modal["blocks"].append({
            "type": "section",
            "block_id": "developers",
            "text": {
                "type": "mrkdwn",
                "text": "Select Developers to invite"
            },
            "accessory": {
                "action_id": "developers",
                "type": "multi_static_select",
                "placeholder": {
                    "type": "plain_text",
                    "text": "Select developers"
                },
                "options": dev_options
            }
        })
    if len(qa_options):
        modal['blocks'].append({
            "type": "section",
            "block_id": "qas",
            "text": {
                "type": "mrkdwn",
                "text": "Select QAs to invite"
            },
            "accessory": {
                "action_id": "qas",
                "type": "multi_static_select",
                "placeholder": {
                    "type": "plain_text",
                    "text": "Select QAs"
                },
                "options": qa_options
            }
        })
    return modal

def command_invite_member(ack, body, logger, client, command):
    try:
        projects_result = get_project_from_channel(command['team_id'], command['user_id'], command['channel_id'])
        if projects_result.get('success', False):
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