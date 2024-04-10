from .payload_helper import register_form_from_payload
from ..events.helpers import handle_home_view
from services.backend.register import register_user

def submit_register(ack, logger, client, body):
    try:
        team = body['team']['id']
        user = body['user']['id']
        form = register_form_from_payload(body['view']['state']['values'], user)
        result = register_user(form)
        if result.get('success', False):
            ack()
            handle_home_view(client, team, user)
        else:
            ack(
                response_action = 'errors',
                errors = {
                    "register_password_block": result.get('message', 'You already have an account!')
                }
            )
    except Exception as e:
        logger.error(f"Error in submit_register: {e}")