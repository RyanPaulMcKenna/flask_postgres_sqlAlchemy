import pytest
from flask import g
from flask import session

from project.extensions import db
from project.modules.users.models import Users

def test_register(client, app):
    # test that successful registration redirects to the login page
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


# def test_login(client, auth):
#     # test that successful login redirects to the index page
#     response = auth.login("test","bestPasswordEver","test.test@gmail.com")

#     # login request set the user_id in the session
#     # check that the user is loaded from the session
#     with client:
#         ping_response = client.get("app/v1/auth/ping")
#         assert ping_response.status_code == 200
        


# @pytest.mark.parametrize(
#     ("username", "password", "message"),
#     (("a", "test", b"Incorrect username."), ("test", "a", b"Incorrect password.")),
# )
# def test_login_validate_input(auth, username, password, message):
#     response = auth.login(username, password)
#     assert message in response.data


# def test_logout(client, auth):
#     auth.login()

#     with client:
#         auth.logout()
#         assert "user_id" not in session
