from ..commands.roll_off import get_roll_off_modal

def roll_off_members(ack, action, client, body):
    project_id = action['value']
    modal = get_roll_off_modal(project_id)
    ack()
    client.views_open(
        trigger_id = body['trigger_id'],
        view = modal
    )