
from .payload_helper import project_form_from_payload
from services.backend.projects import create_project

def get_welcome_message(form):
    new_line = '\n'
    return f'''Welcome to *{form['name']}*!{new_line*2}\
*Project Manager:*{new_line}\
<@{form['project_manager']}>{new_line*2}\
*Developers:*{new_line}\
{new_line.join(map(lambda x: f'<@{x}>', form['developers']))}{new_line*2}\
*QAs:*{new_line}\
{new_line.join(map(lambda x: f'<@{x}>', form['qas']))}{new_line}'''

def submit_create_project(ack, payload, client, context, logger):
    try:
        form = project_form_from_payload(payload['state']['values'])
        form['admin'] = context['user_id']
        create_channel_response = client.conversations_create(
            name = form['channel'],
            team_id = context['team_id'],
            is_private = True
        )
        channel_id = create_channel_response['channel']['id']
        form['channel_id'] = channel_id
        result = create_project(context['team_id'], context['user_id'], form)
        if not result.get('success', False):
            ack(
                response_action = 'errors',
                errors = {
                    'name': 'Session expired! Please log in'
                }
            )
        ack()
        
        users = form['developers'] + form['qas'] + [form['project_manager'], form['admin']]
        client.conversations_setTopic(
            channel = channel_id,
            topic = form['name']
        )
        client.conversations_invite(
            channel = channel_id,
            users = users
        )
        client.chat_postMessage(
            channel=channel_id, 
            text = f"Welcome to {form['name']}",
            blocks = [{
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": get_welcome_message(form)
                    }
            }]
        )
    except Exception as e:
        logger.error(f'Error in submit_create_project: {e.response}')
        ack(
                response_action = 'errors',
                errors = {
                    'channel_name': e.response.get('error', 'Unable to create channel at the moment')
                }
            )