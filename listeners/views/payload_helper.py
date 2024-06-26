import json

def task_form_from_payload(payload, fallback_assignee, project = None):
    form = {
        "title": payload['task_title_block']['task_title_input']['value'],
        "status": payload["selectors"]["task_modal_status_selector"]['selected_option']['value'],
        "eta_done": payload["selectors"]["task_modal_due_date_selector"]['selected_date'],
        "description": json.dumps(payload['task_description_block']['task_description_input']['rich_text_value'])
    }
    if payload['selectors'].get('task_modal_assignee_selector', False):
        form["assignee"] = payload["selectors"]["task_modal_assignee_selector"]['selected_option']['value']
    else:
        form["assignee"] = fallback_assignee
    if project:
        form['project'] = project
    return form

def login_form_from_payload(payload, user):
    form = {
        "username": user,
        "password": payload['login_password_block']['password']['value']
    }
    return form

def register_form_from_payload(payload, user):
    form = {
        "username": user,
        "password": payload['register_password_block']['password']['value'],
        "role": payload['user_role']['user_role']['selected_option']['value']
    }
    return form

def search_form_from_payload(payload):
    form = {}
    if payload['title']['title']['value']:
        form['title'] = {'$regex': payload['title']['title']['value']}
    if len(payload['assignees']['assignees']['selected_options']):
        form['assignee'] = {'$in': [option['value'] for option in payload['assignees']['assignees']['selected_options']]}
    if len(payload['statuses']['statuses']['selected_options']):
        form['status'] = {'$in': list(map(lambda x: x['value'], payload['statuses']['statuses']['selected_options']))}
    if payload['due_date']['min_due_date']['selected_date']:
        form['eta_done'] = {'$gte': payload['due_date']['min_due_date']['selected_date']}
    if payload['due_date']['max_due_date']['selected_date']:
        form['eta_done'] = {'$lte': payload['due_date']['max_due_date']['selected_date']}
    if len(payload['creators']['creators']['selected_options']):
        form['created_by'] = {'$in': [option['value'] for option in payload['creators']['creators']['selected_options']]}
    if payload['created_date']['min_created_date']['selected_date']:
        form['created_at'] = {'$gte': payload['created_date']['min_created_date']['selected_date']}
    if payload['created_date']['max_created_date']['selected_date']:
        form['created_at'] = {'$lte': payload['created_date']['max_created_date']['selected_date']}
    return form

def project_form_from_payload(payload):
    return {
        'details': {
            'name': payload['project_name']['project_name']['value'],
            'channel': payload['channel_name']['channel_name']['value']
        },
        'members': 
            [payload['project_manager']['project_manager']['selected_option']['value']] +
            [option['value'] for option in payload['developers']['developers']['selected_options']] + 
            [option['value'] for option in payload['qas']['qas']['selected_options']],
        'user_by_role': {
            'developers': [option['value'] for option in payload['developers']['developers']['selected_options']],
            'qas': [option['value'] for option in payload['qas']['qas']['selected_options']],
            'project_manager': payload['project_manager']['project_manager']['selected_option']['value']
        }
    }

def invite_members_from_payload(payload):
    members = []
    if payload.get('developers'):
        members.extend([option['value'] for option in payload['developers']['developers']['selected_options']])
    if payload.get('qas'):
        members.extend([option['value'] for option in payload['qas']['qas']['selected_options']])
    return members

def roll_off_members_from_payload(payload):
    members = []
    if payload.get('members'):
        members.extend([option['value'] for option in payload['members']['members']['selected_options']])
    return members