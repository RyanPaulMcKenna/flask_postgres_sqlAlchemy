import pytest
from project.extensions import db
from project.modules.users.models import Users

def test_register(client, app):
    response = client.post("/app/v1/auth/register", json={"username": "ryan","email":"ryan.test@gmail.com", "password": "bestPasswordEver"})
    
    # assert "http://localhost/app/v1/auth/login" == response.headers["Location"]
    with app.app_context():
        from project.modules.users.models import Users
        user = Users.query.filter_by(username="ryan").first()
        # test that the user was inserted into the database
        assert user.username == "ryan"

@pytest.mark.parametrize(
    ("username", "password", "email", "message"),
    (
        ("", "", "", b"Username is required."),
        ("a", "", "", b"Password is required."),
        ("a", "a", "", b"Email is required."),
        ("test", "bestPasswordEver", "test.test@gmail.com", b"Successfully registered"),
        # ("test", "bestPasswordEver", "ryan.test@gmail.com", b"Already registered"),
    ),
)
def test_register_validate_input(client, username, password, email, message):
    response = client.post(
        "app/v1/auth/register", json={"username": username, "password": password, "email": email}
    )
    assert message in response.data


def test_login(client,app, auth):
    register_response = client.post("/app/v1/auth/register", json={"username": "Albert","email":"albert.einstein@gmail.com", "password": "bestPasswordEver"})
    login_response = auth.login("Albert", "bestPasswordEver")
    

    with app.app_context():
        from project.modules.users.models import Users
        user = Users.query.filter_by(username="Albert").first()
        # test that the user was inserted into the database
        assert user.username == "Albert"
        assert register_response.status_code == 200
        assert login_response.status_code == 200

        

@pytest.mark.parametrize(
    ("username", "password", "message"),
    (("a", "test", b"Username or password is invalid."), ("test", "a", b"Username or password is invalid.")),
)
def test_login_validate_input(auth, username, password, message):
    response = auth.login(username, password)
    assert message in response.data


def test_logout(client, auth):
    register_response = client.post("/app/v1/auth/register", json={"username": "Albert","email":"albert.einstein@gmail.com", "password": "bestPasswordEver"})
    login_response = auth.login("Albert", "bestPasswordEver")

    with client:
        login_json = login_response.get_json()
        auth_token = login_json["auth_token"]
        logout_response = auth.logout(auth_token)
        assert logout_response.status_code == 200
