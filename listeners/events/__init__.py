from .app_home_opened import app_home_opened
from .member_joined_channel import member_joined_channel

def register(app):
    app.event("app_home_opened")(app_home_opened)
    app.event("member_joined_channel")(member_joined_channel)
