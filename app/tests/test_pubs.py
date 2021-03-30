import pytest
from project.modules.pubs.models import Pubs
from project.modules.users.models import Users


def test_pubs_get(client, app):
    response = client.get("/app/v1/pubs")

    with app.app_context():
        response_data = response.get_json()["publications"]
        actual_data = Pubs.query.all()

        assert response.status_code == 200
        assert len(response_data) == len(actual_data)

def test_pubs_post(client,app):
    pre_condition_response = client.post("/app/v1/auth/register", json={"username": "Ryan","email":"ryan.test@gmail.com", "password": "bestPasswordEver"})
    assert pre_condition_response.status_code == 200
    
    response = client.post("/app/v1/pubs", json={"name" :"The Test Article", "author": "Ryan", "text":"Hello World!"})

    with app.app_context():
        test_pub = Pubs.query.filter_by(name='The Test Article').first()
        assert response.status_code == 201
        assert test_pub.name == "The Test Article"
        
