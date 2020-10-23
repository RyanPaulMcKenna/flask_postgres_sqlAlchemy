#This is where your intitate app function will be that registers 
#all of the modules (blueprints) to the application when it is imported into
#create app.
from project.modules.users import users_blueprint

def initiate_app(app, **kwargs):
    app.register_blueprint(users_blueprint)