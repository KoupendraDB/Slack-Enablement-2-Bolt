from services.backend.users import get_users

def developers(ack, payload):
    result = get_users({'role': 'developer', 'name': {'$regex': payload['value']}})
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