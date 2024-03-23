def login_button(ack, client, body, logger):
    try:
        ack()
        client.views_open(
            trigger_id = body['trigger_id'],
            view = {
                "title": {
                    "type": "plain_text",
                    "text": "Log in to your account"
                },
                "submit": {
                    "type": "plain_text",
                    "text": "Login",
                },
                "callback_id": "login",
                "blocks": [
                    {
                        "type": "input",
                        "element": {
                            "type": "plain_text_input",
                            "action_id": "username",
                            "placeholder": {
                                "type": "plain_text",
                                "text": "Username"
                            }
                        },
                        "block_id": "login_username_block",
                        "label": {
                            "type": "plain_text",
                            "text": "Username"
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
                        "block_id": "login_password_block",
                        "label": {
                            "type": "plain_text",
                            "text": "Password"
                        }
                    },
                ],
                "type": "modal"
            }
        )
    except Exception as e:
        logger.error(f"Error in login_button: {e}")