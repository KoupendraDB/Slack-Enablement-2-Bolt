from .jwt import store_user_jwt
from .roles import store_user_role
from .request import make_request

def login_user(workspace, user, payload):
    result = make_request(
        name='LOGIN',
        request_type='POST',
        data=payload
    )
    jwt = result.get('access_token', None)
    role = result.get('role', None)
    if jwt:
        store_user_jwt(workspace, user, jwt)
        store_user_role(workspace, user, role)
    return jwt
