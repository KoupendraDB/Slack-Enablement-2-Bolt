from .helpers import submit_new_task_form_from_payload
from services.backend.tasks import create_task

def submit_new_task(ack, logger, body, context, say):
    try:
        form = submit_new_task_form_from_payload(body['view']['state']['values'])
        result = create_task(context['team_id'], context['user_id'], form)
        if result.get('success', False):
            ack()
            say(channel=context['user_id'], blocks=[
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": "Task created successfully!",
                    },
                },
                {
                    "type": "rich_text",
                    "elements": [
                        {
                            "type": "rich_text_section",
                            "elements": [
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
                        }
                    ]
                }
            ],
            text = 'Task created successfully!')
            if context['user_id'] != form['assignee']:
                say(
                    channel = form['assignee'],
                    text=f"<@{context['user_id']}> has assigned you a task!"
                )
        else:
            ack(
                response_action = 'errors',
                errors = {
                    "task_title_block": result.get('message', 'Session expired, please login again!')
                }
            )
    except Exception as e:
        logger.error(f"Error in submit_new_task: {e}")