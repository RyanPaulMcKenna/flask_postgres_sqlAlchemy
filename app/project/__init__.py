import os
from flask import Flask
from http import HTTPStatus

def create_app():
    app = Flask(__name__)

    app.config['DEBUG'] = True

    DBUSER = 'marco'
    DBPASS = 'foobarbaz'
    DBHOST = 'testdb'
    DBPORT = '5432'
    DBNAME = 'mydatabase'

    app.config['SQLALCHEMY_DATABASE_URI'] = \
        'postgresql://{user}:{passwd}@{host}:{port}/{db}'.format(
            user=DBUSER,
            passwd=DBPASS,
            host=DBHOST,
            port=DBPORT,
            db=DBNAME)
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = 'ZQbn05PDeA7v11'

    env_flask_config_name = os.getenv('APP_SETTINGS')
    app.config.from_object(env_flask_config_name)
    
    from . import extensions
    extensions.init_app(app)
    
    from project.models import db, Station
    db.init_app(app)
    
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