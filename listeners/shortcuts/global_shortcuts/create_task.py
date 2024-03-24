from ..helpers import create_task_modal
def global_create_task(ack, body, client, logger):
    try:
        ack()
        user = body['user']['id']
        modal = create_task_modal(user)
        client.views_open(
            trigger_id = body['trigger_id'],
            view = modal
        )
    except Exception as e:
        logger.error(f"Error in global_create_task: {e}")