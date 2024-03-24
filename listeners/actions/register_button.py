def register_button(ack, client, body, logger):
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