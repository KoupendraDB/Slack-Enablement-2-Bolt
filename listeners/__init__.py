from listeners import actions, events, shortcuts, views, commands, options


def register_listeners(app):
    actions.register(app)
    commands.register(app)
    events.register(app)
    options.register(app)
    shortcuts.register(app)
    views.register(app)