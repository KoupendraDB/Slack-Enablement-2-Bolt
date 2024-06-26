from .payload_helper import task_form_from_payload
from services.backend.external import create_task, get_project
from services.backend.aws_s3 import store_files

def get_file_urls_from_payload(payload, task_id):
    files = payload['file_input']['file_input']['files']
    result = {}
    for file in files:
        result[f"{task_id}/{file['name']}"] = file['url_private']
    return result


def submit_new_task(ack, logger, body, context, client, payload):
    try:
        project_id = payload['callback_id'].replace('submit_new_task', '').replace('-', '')
        payload = body['view']['state']['values']
        form = task_form_from_payload(payload, context['user_id'], project_id)
        ack()
        channel_id = form['assignee']
        if project_id:
            project_result = get_project(context['team_id'], context['user_id'], project_id)
            project = project_result['project']
            channel_id = project['channel_id']
        result = create_task(context['team_id'], context['user_id'], form)
        if result.get('success', False):
            files = get_file_urls_from_payload(payload, result['task_id'])
            store_files(files)
            client.chat_postMessage(
                channel = channel_id,
                text=f"<@{context['user_id']}> has created and assigned `{form['title']}` to <@{form['assignee']}>!",
                blocks = [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"<@{context['user_id']}> has created and assigned `{form['title']}` to <@{form['assignee']}>!",
                        },
                        "accessory": {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "View :thinking_face:",
                                "emoji": True
                            },
                            "value": result['task_id'],
                            "action_id": f"view_task_from_message-{result['task_id']}"
                        }
                    }
                ]
                )
        else:
            message_elements = [
                {
                    "type": "text",
                    "text": "Failed to create task "
                },
                {
                    "type": "text",
                    "text": form['title'],
                    "style": {
                        "code": True
                    }
                },
                {
                    "type": "text",
                    "text": ". Please log in!"
                },
            ]
            message_text = 'Failed to create task!'
            client.chat_postEphemeral(
                channel=channel_id,
                user=context['user_id'],
                blocks=[
                    {
                        "type": "rich_text",
                        "elements": [
                            {
                                "type": "rich_text_section",
                                "elements": message_elements
                            }
                        ]
                    }
                ],
                text = message_text
            )
    except Exception as e:
        logger.error(f"Error in submit_new_task: {e}")