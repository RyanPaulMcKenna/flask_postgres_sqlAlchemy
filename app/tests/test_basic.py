import pytest

from project import create_app
from project.extensions import db


@pytest.fixture
def client():
    app = create_app('APP_TEST_SETTINGS')
    
    with app.test_client() as client:
        yield client


def test_something(client):
    
    rv = client.get('/')
    print(rv.data)
    assert b'API' in rv.data