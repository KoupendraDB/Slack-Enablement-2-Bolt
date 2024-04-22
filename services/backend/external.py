from .jwt import fetch_user_jwt, store_user_jwt
from .request import make_request
from .roles import store_user_role
import json

config = {}
with open('./config.json') as config_file:
	config = json.load(config_file)

def get_user_by_username(username):
    result = make_request(
        name='GET_USER_BY_USERNAME',
        url_param={'username': username}
    )
    return result

def register_user(payload):
    result = make_request(
        name='REGISTER_USER',
        data=payload
    )
    return result

def login_user(workspace, user, payload):
    result = make_request(
        name='LOGIN_USER',
        data=payload
    )
    jwt = result.get('access_token', None)
    role = result.get('role', None)
    if jwt:
        store_user_jwt(workspace, user, jwt)
        store_user_role(workspace, user, role)
    return jwt

def get_user_projects(workspace, user):
    jwt = fetch_user_jwt(workspace, user)
    result = make_request(
        name='GET_USER_PROJECTS',
        headers={'bearer-token': jwt},
    )
    return result

def get_user_project_tasks(workspace, user, project_id):
    jwt = fetch_user_jwt(workspace, user)
    result = make_request(
        name='GET_USER_PROJECT_TASKS',
        headers={'bearer-token': jwt},
        url_param={'project_id': project_id}
    )
    return result

def get_user_personal_tasks(workspace, user):
    jwt = fetch_user_jwt(workspace, user)
    result = make_request(
        name='GET_USER_PERSONAL_TASKS',
        headers={'bearer-token': jwt}
    )
    return result

def update_task(workspace, user, task_id, payload):
    jwt = fetch_user_jwt(workspace, user)
    result = make_request(
        name='UPDATE_TASK',
        headers={'bearer-token': jwt},
        url_param={'task_id': task_id},
        data=payload
    )
    return result

def create_task(workspace, user, payload):
    jwt = fetch_user_jwt(workspace, user)
    result = make_request(
        name='CREATE_TASK',
        headers={'bearer-token': jwt},
        data=payload
    )
    return result

def delete_task(workspace, user, task_id):
    jwt = fetch_user_jwt(workspace, user)
    result = make_request(
        name='DELETE_TASK',
        headers={'bearer-token': jwt},
        url_param={'task_id': task_id}
    )
    return result

def get_task(workspace, user, task_id):
    jwt = fetch_user_jwt(workspace, user)
    result = make_request(
        name='GET_TASK',
        headers={'bearer-token': jwt},
        url_param={'task_id': task_id}
    )
    return result

def create_project(workspace, user, payload):
    jwt = fetch_user_jwt(workspace, user)
    result = make_request(
        name='CREATE_PROJECT',
        headers={'bearer-token': jwt},
        data=payload
    )
    return result

def get_project(workspace, user, project_id):
    jwt = fetch_user_jwt(workspace, user)
    result = make_request(
        name='GET_PROJECT',
        headers={'bearer-token': jwt},
        url_param={'project_id': project_id}
    )
    return result

def get_project_by_channel(channel_id):
    result = make_request(
        name='GET_PROJECT_BY_CHANNEL',
        url_param={'channel_id': channel_id}
    )
    return result

def get_project_members(project_id):
    result = make_request(
        name='GET_PROJECT_MEMBERS',
        url_param={'project_id': project_id}
    )
    return result

def accept_project_invite(workspace, user, invitation_code):
    jwt = fetch_user_jwt(workspace, user)
    result = make_request(
        name='ACCEPT_PROJECT_INVITE',
        headers={'bearer-token': jwt},
        url_param={'invitation_code': invitation_code}
    )
    return result

def create_project_invite(workspace, user, project_id, invitee):
    jwt = fetch_user_jwt(workspace, user)
    result = make_request(
        name='CREATE_PROJECT_INVITE',
        headers={'bearer-token': jwt},
        url_param={'project_id': project_id, 'invitee': invitee}
    )
    return result

def roll_off_members(workspace, user, project_id, members):
    jwt = fetch_user_jwt(workspace, user)
    result = make_request(
        name='ROLL_OFF_MEMBERS',
        headers={'bearer-token': jwt},
        data={'members': members},
        url_param={'project_id': project_id}
    )
    return result

def search_tasks(payload):
    result = make_request(
        name='SEARCH_TASKS',
        data=payload
    )
    return result

def get_available_users_by_role(role, name):
    result = make_request(
        name='GET_AVAILABLE_USERS_BY_ROLE',
        url_param={'role': role},
        params={'name': name, 'max_projects': config['max_user_projects']}
    )
    return result