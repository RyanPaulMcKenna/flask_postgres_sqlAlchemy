import os
from flask import Flask
from http import HTTPStatus

def create_app():
    app = Flask(__name__)

    app.config['DEBUG'] = True

    DBUSER = 'marco'
    DBPASS = 'foobarbaz'
    DBHOST = 'db'
    DBPORT = '5432'
    DBNAME = 'mydatabase'

    app.config['SQLALCHEMY_DATABASE_URI'] = \
    'postgresql+psycopg2://{user}:{passwd}@{host}:{port}/{db}'.format(
        user=DBUSER,
        passwd=DBPASS,
        host=DBHOST,
        port=DBPORT,
        db=DBNAME)
    env_flask_config_name = os.getenv('APP_SETTINGS')
    app.config.from_object(env_flask_config_name)

    from project.models import db, Station
    db.init_app(app)

    @app.route('/')
    def main():
        response_object = {
            'status': 'success',
            'users': [station.json() for station in Station.query.all()]
        }
        return response_object, HTTPStatus.OK

    return app