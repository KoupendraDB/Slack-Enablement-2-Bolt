from .helpers import submit_new_task_form_from_payload

def submit_new_task(ack, logger, client, body):
    try:
        ack()
        form = submit_new_task_form_from_payload(body['view']['state']['values'])
        client.chat_postMessage(channel=body['user']['id'], blocks=[
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
    except Exception as e:
        logger.error(f"Error in submit_new_task: {e}")