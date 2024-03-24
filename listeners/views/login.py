from .helpers import login_form_from_payload
from ..events.helpers import handle_home_view
from services.backend.login import login_user

def login(ack, logger, client, body):
    try:
        team = body['team']['id']
        user = body['user']['id']
        form = login_form_from_payload(body['view']['state']['values'], user)
        if login_user(team, user, form):
            ack()
            handle_home_view(client, team, user)
        else:
            ack(
                response_action = 'errors',
                errors = {
                    "login_password_block": 'Invalid credentials!'
                }
            )
    except Exception as e:
        logger.error(f"Error in login: {e}")