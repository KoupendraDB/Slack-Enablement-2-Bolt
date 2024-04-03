from ..shortcuts.helpers import create_task_modal
def create_task(ack, body, client, logger, context):
    try:
        ack()
        user = context['user_id']
        modal = create_task_modal(user)
        client.views_open(
            trigger_id = body["trigger_id"],
            view = modal
        )
    except Exception as e:
        logger.error(f"Error in create_task: {e}")