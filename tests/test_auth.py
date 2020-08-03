import uuid
import pytest
from unittest.mock import patch

from flask import session
from msal import ConfidentialClientApplication

from tools.auth import AuthHandler
from tools.errors import AuthException

def test_unauthed_homepage(app, client):
    """
    Test that the homepage includes a `Click to log in` link
    """
    with app.test_request_context():
        response = client.get("/")
        assert response.status_code == 200
        body = response.data
        assert b"Click to log in" in body

        with client.session_transaction() as session:
            session["user"] = {"name": "Jane"}

        response = client.get("/")
        assert response.status_code == 200

        # This will change when we start rendering templates
        assert response.data == b"Welcome Jane!"


def test_auth_client(app):
    assert isinstance(app.auth, AuthHandler)
    assert isinstance(app.auth.client, ConfidentialClientApplication)

    with app.test_request_context():
        assert app.auth.get_logout_url() == "https://login.microsoftonline.com/ff6254d0-4690-468a-a4ad-828ace3bb668/oauth2/v2.0/logout?post_logout_redirect_uri=http://localhost:8000/"


def test_auth_process(app, client):
    """
    Test the authentication workflow
    """

    with app.test_request_context():
        with patch.object(AuthHandler, "get_auth_url", return_value="https://example.com") as mock_method:
            response = client.get("/")
            assert mock_method.called
            assert response.data == b"<a href='https://example.com'>Click to log in</a>"

        token = uuid.uuid4()
        with patch.object(ConfidentialClientApplication, "acquire_token_by_authorization_code", return_value={"token": token}) as mock_method:
            token_data = app.auth.get_token("mock_code", ["SomeScope.All"], "https://example.com")
            assert token_data.get("token") == token


def test_auth_failure(app):
    with patch.object(ConfidentialClientApplication, "acquire_token_by_authorization_code", return_value={"error": "some error"}) as mock_method:
        with pytest.raises(AuthException):
            token_data = app.auth.get_token("mock_code", ["Scope"], "some_url")

@pytest.mark.skip
def test_unauthed_path():
    pass


@pytest.mark.skip
def test_invalid_auth_request():
    pass
