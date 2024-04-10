from .payload_helper import search_form_from_payload
from services.backend.tasks import search_tasks as search_tasks_service

def tasks_result_modal(tasks):
    blocks = []
    if len(tasks):
        for task in tasks:
            blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"{task['title']}"
                },
                "accessory": {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "View"
                    },
                    "value": f"{task['_id']}",
                    "action_id": f"task_detail_modal-{task['_id']}"
                }
            })
    else:
        blocks.append({
			"type": "section",
			"text": {
				"type": "plain_text",
				"text": "No tasks found :confused:",
				"emoji": True
			}
		})
    modal = {
        "type": "modal",
        "title": {
            "type": "plain_text",
            "text": "Search results"
        },
        "close": {
            "type": "plain_text",
            "text": "Close"
        },
        "blocks": blocks
    }
    return modal

def search_tasks(payload, ack, body, context, client):
    form = search_form_from_payload(payload['state']['values'])
    result = search_tasks_service(context['team_id'], context['user_id'], form)
    if result.get('success', False):
        ack()
        client.views_open(
            trigger_id = body["trigger_id"],
            view = tasks_result_modal(result['tasks'])
        )
    else:
        ack(
            response_action = 'errors',
            errors = {
                "title": 'Session expired! Please refresh'
            }
        )