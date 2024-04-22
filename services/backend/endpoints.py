names = {
    'GET_USER_BY_USERNAME': {
        'METHOD': 'GET',
        'ENDPOINT': "/user/{username}"
    },
    'REGISTER_USER': {
        'METHOD': 'POST',
        'ENDPOINT': "/user/register"
    },
    'LOGIN_USER': {
        'METHOD': 'POST',
        'ENDPOINT': "/user/login"
    },
    'GET_USER_PROJECTS': {
        'METHOD': 'GET',
        'ENDPOINT': "/user/projects"
    },
    'GET_USER_PROJECT_TASKS': {
        'METHOD': 'GET',
        'ENDPOINT': "/user/project/{project_id}/tasks"
    },
    'GET_USER_PERSONAL_TASKS': {
        'METHOD': 'GET',
        'ENDPOINT': "/user/personal/tasks"
    },
    'GET_TASK': {
        'METHOD': 'GET',
        'ENDPOINT': "/task/{task_id}"
    },
    'UPDATE_TASK': {
        'METHOD': 'PATCH',
        'ENDPOINT': "/task/{task_id}"
    },
    'DELETE_TASK': {
        'METHOD': 'DELETE',
        'ENDPOINT': "/task/{task_id}"
    },
    'CREATE_TASK': {
        'METHOD': 'POST',
        'ENDPOINT': "/task"
    },
    'GET_PROJECT': {
        'METHOD': 'GET',
        'ENDPOINT': "/project/{project_id}"
    },
    'CREATE_PROJECT': {
        'METHOD': 'POST',
        'ENDPOINT': "/project"
    },
    'GET_PROJECT_BY_CHANNEL': {
        'METHOD': 'GET',
        'ENDPOINT': "/project/channel/{channel_id}"
    },
    'GET_PROJECT_MEMBERS': {
        'METHOD': 'GET',
        'ENDPOINT': "/project/{project_id}/members"
    },
    'ACCEPT_PROJECT_INVITE': {
        'METHOD': 'POST',
        'ENDPOINT': "/project/accept-invite/{invitation_code}"
    },
    'CREATE_PROJECT_INVITE': {
        'METHOD': 'POST',
        'ENDPOINT': "/project/{project_id}/create-invite"
    },
    'ROLL_OFF_MEMBERS': {
        'METHOD': 'POST',
        'ENDPOINT': "/project/{project_id}/roll-of-members"
    },
    'SEARCH_TASKS': {
        'METHOD': 'GET',
        'ENDPOINT': "/tasks"
    },
    'GET_AVAILABLE_USERS_BY_ROLE': {
        'METHOD': 'GET',
        'ENDPOINT': "/users/available/{role}"
    }
}