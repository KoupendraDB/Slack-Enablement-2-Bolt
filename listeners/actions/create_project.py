def get_create_project_modal():
    return {
        "type": "modal",
        "title": {
            "type": "plain_text",
            "text": "Create a Project"
        },
        "submit": {
            "type": "plain_text",
            "text": "Create"
        },
        "close": {
            "type": "plain_text",
            "text": "Cancel"
        },
        "callback_id": "submit_create_project",
        "blocks": [
            {
                "type": "input",
                "block_id": "project_name",
                "element": {
                    "type": "plain_text_input",
                    "action_id": "project_name",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Name"
                    }
                },
                "label": {
                    "type": "plain_text",
                    "text": "Project Name"
                }
            },
            {
                "type": "input",
                "block_id": "project_manager",
                "element": {
                    "type": "external_select",
                    "min_query_length": 0,
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Select Project Manager"
                    },
                    "action_id": "project_manager"
                },
                "label": {
                    "type": "plain_text",
                    "text": "Project Manager"
                }
            },
            {
                "type": "input",
                "block_id": "developers",
                "element": {
                    "type": "multi_external_select",
                    "min_query_length": 0,
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Select developers"
                    },
                    "action_id": "developers"
                },
                "label": {
                    "type": "plain_text",
                    "text": "Developers"
                }
            },
            {
                "type": "input",
                "block_id": "qas",
                "element": {
                    "type": "multi_external_select",
                    "min_query_length": 0,
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Select QAs"
                    },
                    "action_id": "qas"
                },
                "label": {
                    "type": "plain_text",
                    "text": "QAs"
                }
            },
            {
                "type": "input",
                "block_id": "channel_name",
                "element": {
                    "type": "plain_text_input",
                    "action_id": "channel_name",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Example: test-project-123"
                    }
                },
                "label": {
                    "type": "plain_text",
                    "text": "Channel Name"
                }
            }
        ]
    }

def create_project(ack, client, body):
    ack()
    client.views_open(
        trigger_id = body['trigger_id'],
        view = get_create_project_modal()
    )