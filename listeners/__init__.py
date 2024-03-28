from listeners import actions, events, shortcuts, views, commands


def register_listeners(app):
    actions.register(app)
    commands.register(app)
    events.register(app)
    shortcuts.register(app)
    views.register(app)