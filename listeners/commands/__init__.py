from .create_task import command_create_task
from .invite import command_invite_member
from .roll_off import command_roll_off


def register(app):
    app.command("/tm-create-task")(command_create_task)
    app.command("/tm-invite")(command_invite_member)
    app.command("/tm-roll-off")(command_roll_off)
