def delete_task_action(ack, body, action, client):
    ack()
    task_id = action['value']
    client.views_open(
        trigger_id = body["trigger_id"],
        view = {
            "title": {
                "type": "plain_text",
                "text": "Delete Task"
            },
            "submit": {
                "type": "plain_text",
                "text": "Yes, sure",
            },
            "callback_id": f"delete_task-{task_id}",
            "blocks": [
                {
                    "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"Are you sure you want to delete this task?",\
                        }
                }
            ],
            "type": "modal"
        }
    )