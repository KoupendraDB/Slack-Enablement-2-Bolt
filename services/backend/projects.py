from .jwt import fetch_user_jwt
from .request import make_request

def get_user_projects(workspace, user):
    jwt = fetch_user_jwt(workspace, user)
    result = make_request(
        name='GET_USER_PROJECTS',
        request_type='GET',
        headers={'bearer-token': jwt},
        url_param={'user_id': user}
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