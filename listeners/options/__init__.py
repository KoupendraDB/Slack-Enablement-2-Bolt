from .project_managers import project_managers
from .developers import developers
from .qas import qas

def register(app):
    app.options("project_manager")(project_managers)
    app.options("developers")(developers)
    app.options("qas")(qas)