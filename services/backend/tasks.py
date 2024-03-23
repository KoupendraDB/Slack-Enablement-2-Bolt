from .helper import fetch_user_jwt
from .request import make_request

def get_tasks(workspace, user):
    jwt = fetch_user_jwt(workspace, user)
    result = make_request(
        name='GET_TASKS',
        request_type='GET',
        headers={'bearer-token': jwt}
    )
    return result
