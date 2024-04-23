from ..commands.invite import get_invite_member_modal

def invite_members(ack, action, client, body):
    project_id = action['value']
    modal = get_invite_member_modal(project_id)
    ack()
    client.views_open(
        trigger_id = body['trigger_id'],
        view = modal
    )