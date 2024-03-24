import json

def submit_new_task_form_from_payload(payload):
    form = {
        "title": payload['task_title_block']['task_title_input']['value'],
        "assignee": payload["selectors"]["assignee_selector"]['selected_user'],
        "eta_done": payload["selectors"]["due_date_selector"]['selected_date'],
        "description": json.dumps(payload['task_description_block']['task_description_input']['rich_text_value'])
    }
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