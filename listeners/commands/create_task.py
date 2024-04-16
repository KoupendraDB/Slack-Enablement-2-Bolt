from services.backend.projects import get_project_from_channel
from ..actions.task_modal import get_create_task_modal

def command_create_task(ack, client, command, logger, body):
    try:
        ack()
        projects_result = get_project_from_channel(command['team_id'], command['user_id'], command['channel_id'])
        if projects_result.get('success', False):
            projects = projects_result['projects']
            if len(projects) > 0:
                project = projects[0]
                modal = get_create_task_modal(command, client, project['_id'], project=project)
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
        else:
            client.chat_postEphemeral(
                channel=command['channel_id'],
                user=command['user_id'],
                text = "Session expired! Please login to the Task Manager app!"
            )
            
    except Exception as e:
        logger.error(f"Error in command_create_task: {e}")