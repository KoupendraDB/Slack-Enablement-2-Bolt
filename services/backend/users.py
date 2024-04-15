from .request import make_request

def get_users(payload):
    result = make_request(
        name='SEARCH_USERS',
        request_type='GET',
        data=payload
    )
    return result