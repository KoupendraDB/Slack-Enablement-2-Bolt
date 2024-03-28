from .helpers import submit_new_task_form_from_payload
from services.backend.tasks import create_task

def submit_new_task(ack, logger, body, context, client):
    try:
        form = submit_new_task_form_from_payload(body['view']['state']['values'])
        ack()
        result = create_task(context['team_id'], context['user_id'], form)
        if result.get('success', False):
            message_elements = [
                                {
                                    "type": "text",
                                    "text": "New task "
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
                                    "text": " has been created successfully!"
                                }
                            ]
            if context['user_id'] != form['assignee']:
                client.chat_postMessage(
                    channel = form['assignee'],
                    text=f"<@{context['user_id']}> has assigned you a task!"
                )
            message_text = 'Task created successfully!'
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
            channel=context['user_id'],
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