from services.backend.external import get_project_by_channel
from ...actions.task_modal import get_create_task_modal

def message_create_task(ack, payload, client, logger, context, shortcut):
    try:
        ack()
        channel_id = shortcut['channel']['id']
        result = get_project_by_channel(channel_id)
        project = result.get('project')
        if project:
            message_blocks = payload["message"]['blocks']
            for block in message_blocks:
                if block["type"] == "rich_text":
                    description = block
                    break
            modal = get_create_task_modal(context, project['_id'], description, project)
            client.views_open(
                trigger_id = payload['trigger_id'],
                view = modal
            )
        else:
            client.chat_postEphemeral(
                channel=channel_id,
                user=context['user_id'],
                text = "Project isn't associated with the Task Manager app!"
            )
    except Exception as e:
        logger.error(f"Error in message_create_task: {e}")