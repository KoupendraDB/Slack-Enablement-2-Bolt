from ..events.helpers import get_task_status_options

def search_tasks_modal():
    modal = {
        "type": "modal",
        "title": {
            "type": "plain_text",
            "text": "Search tasks"
        },
        "submit": {
            "type": "plain_text",
            "text": "Search"
        },
        "close": {
            "type": "plain_text",
            "text": "Close"
        },
        "callback_id": "search_tasks",
        "blocks": [
            {
                "type": "divider"
            },
            {
                "type": "input",
                "block_id": "title",
                "element": {
                    "type": "plain_text_input",
                    "action_id": "title",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Title"
                    }
                },
                "optional": True,
                "label": {
                    "type": "plain_text",
                    "text": "Title"
                }
            },
            {
                "type": "input",
                "block_id": "assignees",
                "element": {
                    "type": "multi_users_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Select assignees"
                    },
                    "action_id": "assignees"
                },
                "optional": True,
                "label": {
                    "type": "plain_text",
                    "text": "Assignee"
                }
            },
            {
                "type": "input",
                "block_id": "statuses",
                "optional": True,
                "element": {
                    "type": "multi_static_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Select options"
                    },
                    "options": get_task_status_options(),
                    "action_id": "statuses"
                },
                "label": {
                    "type": "plain_text",
                    "text": "Status"
                }
            },
            {
                "type": "actions",
                "block_id": "due_date",
                "elements": [
                    {
                        "type": "datepicker",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Minimum Due Date"
                        },
                        "action_id": "min_due_date"
                    },
                    {
                        "type": "datepicker",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Maximum Due Date"
                        },
                        "action_id": "max_due_date"
                    }
                ]
            },
            {
                "type": "input",
                "block_id": "creators",
                "element": {
                    "type": "multi_users_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Select creators"
                    },
                    "action_id": "creators"
                },
                "optional": True,
                "label": {
                    "type": "plain_text",
                    "text": "Creators"
                }
            },
            {
                "type": "actions",
                "block_id": "created_date",
                "elements": [
                    {
                        "type": "datepicker",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Minimum Created Date"
                        },
                        "action_id": "min_created_date"
                    },
                    {
                        "type": "datepicker",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Maximum Created Date"
                        },
                        "action_id": "max_created_date"
                    }
                ]
            },
        ]
    }
    return modal

def search_tasks(ack, body, client, logger):
    try:
        ack()
        modal = search_tasks_modal()
        client.views_open(
            trigger_id = body["trigger_id"],
            view = modal
        )
    except Exception as e:
        logger.error(f"Error in search_tasks_modal: {e}")