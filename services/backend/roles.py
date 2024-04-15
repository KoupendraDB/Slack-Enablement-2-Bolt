def fetch_user_role(workspace, user):
    from app import mongo_client
    key = f"{workspace}:{user}"
    result = mongo_client.SlackApp.jwt.find_one({'key': key}, {'_id': 0})
    return result['role'] if result else None

def store_user_role(workspace, user, role):
    from app import mongo_client
    key = f"{workspace}:{user}"
    mongo_client.SlackApp.jwt.update_one(
        {'key': key},
        {'$set': {'key': key, 'role': role}},
        upsert=True
    )
