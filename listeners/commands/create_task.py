from .helpers import get_create_task_form_from_payload
from services.backend.tasks import create_task

def command_create_task(ack, respond, command, say):
    form = get_create_task_form_from_payload(command['text'], command['user_id'])
    ack()
    if form:
        result = create_task(command['team_id'], command['user_id'], form)
        if result.get('success', False):
            respond(f"New task `{form['title']}` has been created successfully!")
            if command['user_id'] != form['assignee']:
                say(
                    channel=form['assignee'],
                    text=f"<@{command['user_id']}> has assigned you a task!"
                )
        else:
            respond(f"Failed to create task `{form['title']}`. Please log in!")
    else:
        respond(f"Failed to create task. Please populate `Title` and `Description` fields!")
    