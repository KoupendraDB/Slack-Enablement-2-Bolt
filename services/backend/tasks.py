from .helper import fetch_user_jwt
from .request import make_request

def get_tasks(workspace, user):
    jwt = fetch_user_jwt(workspace, user)
    result = make_request(
        name='GET_TASKS',
        request_type='GET',
        headers={'bearer-token': jwt},
        params={'assignee_$eq': user}
    )
    return result

def update_task(task_id, workspace, user, payload):
    jwt = fetch_user_jwt(workspace, user)
    result = make_request(
        name='PATCH_TASK',
        request_type='PATCH',
        headers={'bearer-token': jwt},
        url_param={'task_id': task_id},
        data=payload
    )
    return result