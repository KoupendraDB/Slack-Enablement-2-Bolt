from services.backend.users import get_users

def project_managers(ack, payload):
    result = get_users({'role': 'project_manager', 'name': payload['value']})
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