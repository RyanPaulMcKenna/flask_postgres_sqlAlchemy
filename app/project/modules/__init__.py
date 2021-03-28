# This is where your intitate app function will be that registers
# all of the modules (blueprints) to the application when it is imported into
# create app.
from project.modules.auth import api as authApi
from project.modules.users import users_blueprint as usersApi


def initiate_app(app, **kwargs):
    app.register_blueprint(authApi)
    app.register_blueprint(usersApi)