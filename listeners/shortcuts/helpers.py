from datetime import date

def create_task_modal(message, user):
    modal = {
        "title": {
            "type": "plain_text",
            "text": "Create Task"
        },
        "submit": {
            "type": "plain_text",
            "text": "Create",
        },
        "callback_id": "submit_new_task",
        "blocks": [
            {
                "type": "input",
                "element": {
                    "type": "plain_text_input",
                    "action_id": "task_title_input",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Task title"
                    }
                },
                "block_id": "task_title_block",
                "label": {
                    "type": "plain_text",
                    "text": "Title"
                }
            },
            {
                "type": "input",
                "block_id": "task_description_block",
                "element": {
                    "type": "plain_text_input",
                    "action_id": "task_description_input",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Task description"
                    },
                    "multiline": True,
                    "initial_value": message
                },
                "label": {
                    "type": "plain_text",
                    "text": "Description"
                }
            },
            {
                "type": "actions",
                "block_id": "selectors",
                "elements": [
                    {
                        "type": "users_select",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Select a user",
                            "emoji": True
                        },
                        "initial_user": user,
                        "action_id": "assignee_selector"
                    },
                    {
                        "type": "datepicker",
                        "initial_date": date.today().isoformat(),
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Select a due date",
                            "emoji": True
                        },
                        "action_id": "due_date_selector"
                    }
                ]
            }
        ],
        "type": "modal"
    }
    return modal
