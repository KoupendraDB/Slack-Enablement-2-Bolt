def join_project(ack, body, client):
    ack()
    client.views_open(
        trigger_id=body['trigger_id'],
        view={
            "title": {
                "type": "plain_text",
                "text": "Join a Project"
            },
            "submit": {
                "type": "plain_text",
                "text": "Submit",
            },
            "callback_id": f"submit_join_project",
            "blocks": [
                {
                    "type": "input",
                    "block_id": "invite_code",
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "invite_code"
                    },
                    "label": {
                        "type": "plain_text",
                        "text": "Enter invite code",
                    }
		        }
            ],
            "type": "modal"
        }
    )
