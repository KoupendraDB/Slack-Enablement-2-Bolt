from services.backend.external import get_project

def archive_project(ack, client, action, body, context):
    ack()
    project_id = action['value']
    result = get_project(context['team_id'], context['user_id'], project_id)
    if result.get('success', False):
        project = result['project']
        client.views_open(
            trigger_id = body['trigger_id'],
            view = {
                "type": "modal",
                "title": {
                    "type": "plain_text",
                    "text": "Archive Project"
                },
                "submit": {
                    "type": "plain_text",
                    "text": "Archive"
                },
                "callback_id": f"submit_archive_project-{project_id}",
                "blocks": [
                    {
                        "type": "divider"
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"*Are you sure you want to proceed archiving project: `{project['name']}`?*\n\nArchiving a project will release all the members from the project and archive the channel <#{project['channel_id']}>"
                        }
                    }
                ]
            }
        )