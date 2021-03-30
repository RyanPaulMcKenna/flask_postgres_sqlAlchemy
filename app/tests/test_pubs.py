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
        

def test_pubs_put(client, app):
    pre_condition_one_response = client.post("/app/v1/auth/register", json={"username": "Ryan","email":"ryan.test@gmail.com", "password": "bestPasswordEver"})
    assert pre_condition_one_response.status_code == 200
    
    pre_condition_two_response = client.post("/app/v1/pubs", json={"name" :"The Test Article", "author": "Ryan", "text":"Hello World!"})
    assert pre_condition_two_response.status_code == 201

    with app.app_context():
        test_pub = Pubs.query.filter_by(name='The Test Article').first()
        assert test_pub.name == "The Test Article"
        assert test_pub.text == "Hello World!"

        new_name = "The Altered Test Article"
        new_text = "Hello Mars!"

        response = client.put("/app/v1/pubs", json={"id": test_pub.id, "name" : new_name, "author": "Ryan", "text": new_text})
        test_pub_altered = Pubs.query.filter_by(name=new_name).first()

        assert response.status_code == 201
        assert test_pub.id == test_pub_altered.id
        assert test_pub_altered.name == new_name
        assert test_pub_altered.text == new_text

        
