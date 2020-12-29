import os
from http import HTTPStatus

from flask import Flask
from flask_restx import Api
from werkzeug.middleware.proxy_fix import ProxyFix

def create_app(config=None):
    config_name = ''
    if config == None:
       config_name = 'APP_SETTINGS'
    else:
        config_name = 'APP_TEST_SETTINGS'
    
    app = Flask(__name__)
    app.wsgi_app = ProxyFix(app.wsgi_app)

    api = Api(app)

    env_flask_config_name = os.getenv(config_name)
    app.config.from_object(env_flask_config_name)

    from . import extensions
    extensions.init_app(app)

    from project.models import Station

    from . import modules
    modules.initiate_app(app)

    @app.route('/app')
    def main():
        response_object = {
            'status': 'success',
            'users': [station.json() for station in Station.query.all()]
        }
        return response_object, HTTPStatus.OK

    return app
