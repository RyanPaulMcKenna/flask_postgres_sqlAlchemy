import os
from http import HTTPStatus

from flask import Flask
from flask_restx import Api
from werkzeug.middleware.proxy_fix import ProxyFix

def create_app(config=None):
    app = Flask(__name__)
    app.wsgi_app = ProxyFix(app.wsgi_app)

    api = Api(app)

    env_flask_config = os.getenv('APP_SETTINGS')
    app.config.from_object(env_flask_config)

    from . import extensions
    extensions.init_app(app)

    from project.modules.files.models import Files

    from . import modules
    modules.initiate_app(app)

    @app.route('/app')
    def main():
        response_object = {
            'status': 'success',
            'files': [file.to_json() for file in Files.query.all()]
        }
        return response_object, HTTPStatus.OK

    return app
