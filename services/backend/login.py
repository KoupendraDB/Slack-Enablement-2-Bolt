from .jwt import store_user_jwt
from .request import make_request

def login_user(workspace, user, payload):
    result = make_request(
        name='LOGIN',
        request_type='POST',
        data=payload
    )
    jwt = result.get('access_token', None)
    if jwt:
        store_user_jwt(workspace, user, jwt)
    return jwt
