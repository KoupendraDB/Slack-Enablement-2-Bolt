import json

def task_form_from_payload(payload, fallback_assignee):
    form = {
        "title": payload['task_title_block']['task_title_input']['value'],
        "status": payload["selectors"]["task_modal_status_selector"]['selected_option']['value'],
        "eta_done": payload["selectors"]["task_modal_due_date_selector"]['selected_date'],
        "description": json.dumps(payload['task_description_block']['task_description_input']['rich_text_value'])
    }
    if payload['selectors'].get('task_modal_assignee_selector', False):
        form["assignee"] = payload["selectors"]["task_modal_assignee_selector"]['selected_user']
    else:
        form["assignee"] = fallback_assignee
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
        "password": payload['register_password_block']['password']['value']
    }
    return form

def search_form_from_payload(payload):
    form = {}
    if payload['title']['title']['value']:
        form['title_$regex'] = payload['title']['title']['value']
    if len(payload['assignees']['assignees']['selected_users']):
        form['assignee_$in'] = ','.join(payload['assignees']['assignees']['selected_users'])
    if len(payload['statuses']['statuses']['selected_options']):
        form['status_$in'] = ','.join(list(map(lambda x: x['value'], payload['statuses']['statuses']['selected_options'])))
    if payload['due_date']['min_due_date']['selected_date']:
        form['eta_done_$gte'] = payload['due_date']['min_due_date']['selected_date']
    if payload['due_date']['max_due_date']['selected_date']:
        form['eta_done_$lte'] = payload['due_date']['max_due_date']['selected_date']
    if len(payload['creators']['creators']['selected_users']):
        form['created_by_$in'] = ','.join(payload['creators']['creators']['selected_users'])
    if payload['created_date']['min_created_date']['selected_date']:
        form['created_at_$gte'] = payload['created_date']['min_created_date']['selected_date']
    if payload['created_date']['max_created_date']['selected_date']:
        form['created_at_$lte'] = payload['created_date']['max_created_date']['selected_date']
    return form