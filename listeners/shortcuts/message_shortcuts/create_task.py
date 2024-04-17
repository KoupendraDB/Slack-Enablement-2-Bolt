from services.backend.projects import get_project_from_channel
from ...actions.task_modal import get_create_task_modal

def message_create_task(ack, payload, client, logger, context, shortcut):
    try:
        ack()
        channel_id = shortcut['channel']['id']
        projects_result = get_project_from_channel(context['team_id'], context['user_id'], channel_id)
        project_id, project = None, None
        if projects_result.get('success', False):
            projects = projects_result['projects']
            if len(projects) > 0:
                project_id, project = projects[0]['_id'], projects[0]
                message_blocks = payload["message"]['blocks']
                for block in message_blocks:
                    if block["type"] == "rich_text":
                        description = block
                        break
                modal = get_create_task_modal(context, client, project_id, description, project)
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
        else:
            client.chat_postEphemeral(
                channel=channel_id,
                user=context['user_id'],
                text = "Session expired! Please login to the Task Manager app!"
            )
    except Exception as e:
        logger.error(f"Error in message_create_task: {e}")