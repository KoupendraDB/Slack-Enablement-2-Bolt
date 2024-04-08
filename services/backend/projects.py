from .helper import fetch_user_jwt
from .request import make_request

def get_user_projects(workspace, user):
    jwt = fetch_user_jwt(workspace, user)
    result = make_request(
        name='GET_USER_PROJECTS',
        request_type='GET',
        headers={'bearer-token': jwt}
    )
    return result