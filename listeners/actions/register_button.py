role_options = [
    {
        "text": {
            "type": "plain_text",
            "text": "Project Manager",
        },
        "value": "project_manager"
    },
    {
        "text": {
            "type": "plain_text",
            "text": "Developer",
        },
        "value": "developer"
    },
    {
        "text": {
            "type": "plain_text",
            "text": "QA",
        },
        "value": "qa"
    }
]

def register_button(ack, client, body, logger, context):
    try:
        ack()
        client.views_open(
            trigger_id = body['trigger_id'],
            view = {
                "title": {
                    "type": "plain_text",
                    "text": "Register an account"
                },
                "submit": {
                    "type": "plain_text",
                    "text": "Register",
                },
                "callback_id": "submit_register",
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"Username: *{context['user_id']}*"
                        }
                    },
                    {
                        "type": "input",
                        "block_id": "user_role",
                        "element": {
                            "type": "static_select",
                            "placeholder": {
                                "type": "plain_text",
                                "text": "Select a role",
                            },
                            "options": role_options,
                            "action_id": "user_role"
                        },
                        "label": {
                            "type": "plain_text",
                            "text": "Role",
                        }
                    },
                    {
                        "type": "input",
                        "element": {
                            "type": "plain_text_input",
                            "action_id": "password",
                            "placeholder": {
                                "type": "plain_text",
                                "text": "Password"
                            }
                        },
                        "block_id": "register_password_block",
                        "label": {
                            "type": "plain_text",
                            "text": "Password"
                        }
                    }
                ],
                "type": "modal"
            }
        )
    except Exception as e:
        logger.error(f"Error in register_button: {e}")