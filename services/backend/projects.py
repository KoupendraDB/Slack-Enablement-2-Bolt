from .jwt import fetch_user_jwt
from .request import make_request

def get_user_projects(workspace, user):
    jwt = fetch_user_jwt(workspace, user)
    payload = {'$or': [
        {'project_manager': user},
        {'developers': {'$elemMatch': {'$eq': user}}},
        {'qas': {'$elemMatch': {'$eq': user}}}
    ]}
    result = make_request(
        name='GET_PROJECTS',
        request_type='GET',
        headers={'bearer-token': jwt},
        data=payload
    )
    return result

def create_project(workspace, user, payload):
    jwt = fetch_user_jwt(workspace, user)
    result = make_request(
        name='CREATE_PROJECT',
        request_type='POST',
        headers={'bearer-token': jwt},
        data=payload
    )
    return result

def get_project(workspace, user, project_id):
    jwt = fetch_user_jwt(workspace, user)
    result = make_request(
        name='GET_PROJECT',
        request_type='GET',
        headers={'bearer-token': jwt},
        url_param={'project_id': project_id}
    )
    return result

def update_project(workspace, user, project_id, payload):
    jwt = fetch_user_jwt(workspace, user)
    result = make_request(
        name='UPDATE_PROJECT',
        request_type='PATCH',
        headers={'bearer-token': jwt},
        data=payload,
        url_param={'project_id': project_id}
    )
    return result