from services.backend.users import get_users

def qas(ack, payload):
    result = get_users({
        'role': 'qa',
        'name': {'$regex': payload['value']},
        'projects': {
            '$exists': True,
            '$size': 0
        }
    })
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