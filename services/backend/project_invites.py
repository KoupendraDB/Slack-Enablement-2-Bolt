from bson import ObjectId

def create_project_invite_code(projectId, members):
    from app import mongo_client
    insert_result = mongo_client.SlackApp.invites.insert_one({
        'projectId': projectId,
        'members': members
    })
    return str(insert_result.inserted_id)

def get_projectId_from_invite_code(code, user):
    from app import mongo_client
    try:
        invite_code = ObjectId(code)
        result = mongo_client.SlackApp.invites.find_one({
            '_id': invite_code,
            'members': {'$elemMatch': {'$eq': user}}
        })
        if result:
            return result['projectId']
    except Exception as e:
        print(e)
    return