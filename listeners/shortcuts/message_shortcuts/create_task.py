from ..helpers import create_task_modal
def message_create_task(ack, body, client, logger):
    try:
        ack()
        description = body['message']['blocks'][0]['elements'][0]['elements'][0]['text']
        user = body['user']['id']
        modal = create_task_modal(description, user)
        client.views_open(
            trigger_id = body['trigger_id'],
            view = modal
        )
    except Exception as e:
        logger.error(f"Error in message_create_task: {e}")