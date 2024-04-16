from .create_task import command_create_task
from .invite import command_invite_member


def register(app):
    app.command("/tm-create-task")(command_create_task)
    app.command("/tm-invite")(command_invite_member)
