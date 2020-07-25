import pytest
import json

from tools.errors import AppException


def raise_exception():
    raise AppException("This is not allowed")


class Unrecoverable(Exception):
    pass


def test_app_exception(app, client):
    app.add_url_rule("/raise", "raise", raise_exception)

    response = client.get("/raise")
    assert json.loads(response.data) == {"message": "This is not allowed"}

    with pytest.raises(Exception):  # Makes sure the test passes
        with pytest.raises(AppException):  # Try to catch an unrecoverable error
            raise Unrecoverable("Too bad")
