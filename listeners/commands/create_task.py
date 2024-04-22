from services.backend.external import get_project_by_channel
from ..actions.task_modal import get_create_task_modal

def command_create_task(ack, client, command, logger, body):
    try:
        ack()
        result = get_project_by_channel(command['channel_id'])
        project = result.get('project')
        if project:
            modal = get_create_task_modal(command, project['_id'], project=project)
            client.views_open(
                trigger_id = body['trigger_id'],
                view = modal
            )
        else:
            client.chat_postEphemeral(
                channel=command['channel_id'],
                user=command['user_id'],
                text = "Project isn't associated with the Task Manager app!"
            )
            
    except Exception as e:
        logger.error(f"Error in command_create_task: {e}")