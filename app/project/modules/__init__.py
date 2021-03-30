# This is where your intitate app function will be that registers
# all of the modules (blueprints) to the application when it is imported into
# create app.
from project.modules.auth import auth_api
from project.modules.users import users_blueprint
from project.modules.files import files_blueprint
from project.modules.pubs import pubs_blueprint

def initiate_app(app, **kwargs):
    app.register_blueprint(auth_api)
    app.register_blueprint(users_blueprint)
    app.register_blueprint(files_blueprint)
    app.register_blueprint(pubs_blueprint)
