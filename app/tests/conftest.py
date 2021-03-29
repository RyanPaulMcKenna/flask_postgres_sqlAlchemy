import pytest
import os
from project import create_app
from project.extensions import db
# from flask_sqlalchemy import SQLAlchemy

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    # create the app with common test config
    app = create_app()
    # create the database and load test data
    with app.app_context():
        db.drop_all()
        db.create_all()
        db.session.commit()
    yield app


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()


class AuthActions:
    def __init__(self, client):
        self._client = client

    def register(self, username="test", password="test", email="test"):
        return self._client.post(
            "app/v1/auth/register", json={"username": username,"email": email,"password": password}
        )

    def login(self, username="test", password="test", email="test"):
        return self._client.post(
            "app/v1/auth/login", json={"username": username, "password": password}
        )

    def logout(self,authorization):
        return self._client.get("app/v1/auth/logout", headers={"Authorization": "Basic " + authorization})


@pytest.fixture
def auth(client):
    return AuthActions(client)
