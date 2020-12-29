import pytest
import os

from project import create_app
from project.extensions import db

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    # create the app with common test config
    app = create_app({"TESTING": True})
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

    def login(self, username="test", password="test", email="test"):
        return self._client.post(
            "/auth/v1/login", data={"username": username,"email": email,"password": password}
        )

    def logout(self):
        return self._client.get("/auth/v1/logout")


@pytest.fixture
def auth(client):
    return AuthActions(client)
