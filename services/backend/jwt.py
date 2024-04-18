def fetch_user_jwt(workspace, user):
    from app import mongo_client
    key = f"{workspace}:{user}"
    result = mongo_client.SlackApp.jwt.find_one({'key': key}, {'_id': 0})
    return result['jwt'] if result else None

def store_user_jwt(workspace, user, jwt):
    from app import mongo_client
    key = f"{workspace}:{user}"
    mongo_client.SlackApp.jwt.update_one(
        {'key': key},
        {'$set': {'key': key, 'jwt': jwt}},
        upsert=True
    )

