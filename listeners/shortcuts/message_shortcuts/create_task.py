from ..helpers import create_task_modal
def message_create_task(ack, payload, client, logger):
    try:
        ack()
        message_blocks = payload["message"]['blocks']
        for block in message_blocks:
            if block["type"] == "rich_text":
                description = block
        user = payload['user']['id']
        modal = create_task_modal(user, description)
        client.views_open(
            trigger_id = payload['trigger_id'],
            view = modal
        )
    except Exception as e:
        logger.error(f"Error in message_create_task: {e}")