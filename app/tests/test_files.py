import pytest
from project.modules.files.models import Files
import os
import json
from io import BytesIO

def test_files_get(client, app):
    response = client.get("/app/v1/files")

    with app.app_context():
        response_data = response.get_json()["files"]
        actual_data = Files.query.all()

        assert response.status_code == 200
        assert len(response_data) == len(actual_data)

def test_files_post(client, app):
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'mocks/file.txt')
    test_file = open(filename,"rb")

    response = client.post("/app/v1/files", content_type="multipart/form-data", data={"name": "file.txt","extension":".txt", "upload": BytesIO(test_file.read())})
    
    with app.app_context():
        assert response.status_code == 201
        assert json.loads(response.get_data())['message'] == 'file was added.'
        file = Files.query.filter_by(name='file.txt').first()
        assert file.name == "file.txt"