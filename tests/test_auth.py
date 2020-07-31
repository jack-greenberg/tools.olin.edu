import json
import pytest
from unittest.mock import patch

from tools.auth import AuthHandler

def test_unauthed_homepage(client):
    """
    Test that the homepage includes a `Click to log in` link
    """
    response = client.get("/")
    assert response.status_code == 200
    body = response.data
    assert b"Click to log in" in body

def test_auth_process(app, client):
    """
    Test the authentication workflow
    """
    assert isinstance(app.auth, AuthHandler)


@pytest.mark.skip
def test_auth_failure():
    pass

@pytest.mark.skip
def test_unauthed_path():
    pass

@pytest.mark.skip
def test_invalid_auth_request():
    pass
