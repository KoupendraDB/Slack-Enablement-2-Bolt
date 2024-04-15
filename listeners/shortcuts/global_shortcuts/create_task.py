from ...actions.task_modal import get_create_task_modal

def global_create_task(ack, body, client, logger, context):
    try:
        ack()
        modal = get_create_task_modal(context, client)
        client.views_open(
            trigger_id = body['trigger_id'],
            view = modal
        )
    except Exception as e:
        logger.error(f"Error in global_create_task: {e}")