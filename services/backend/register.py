from .request import make_request

def register_user(payload):
    result = make_request(
        name='REGISTER',
        request_type='POST',
        data=payload
    )
    return result
