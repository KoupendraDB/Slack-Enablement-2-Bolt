from services.backend.external import get_available_users_by_role

def developers(ack, payload):
    result = get_available_users_by_role('developer', payload['value'])
    users = result.get('users', [])
    ack(options=[
        {
            "text": {
                "type": "plain_text",
                "text": user['name']
            },
            "value": user['username']
        }
    for user in users])