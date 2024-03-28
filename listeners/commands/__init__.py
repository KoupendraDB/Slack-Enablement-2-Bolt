from .create_task import command_create_task


def register(app):
    app.command("/create-task")(command_create_task)
