from .global_shortcuts.create_task import global_create_task
from .message_shortcuts.create_task import message_create_task


def register(app):
    # Global shortcuts
    app.shortcut("global_create_task")(global_create_task)

    # Message shortcuts
    app.shortcut("message_create_task")(message_create_task)
    