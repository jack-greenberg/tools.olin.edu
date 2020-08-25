import pytest
from flask_jwt_extended import create_access_token

from tools.utils import Role
from tools.database.models import User
from tools.auth import scoped


@pytest.fixture
def ninja_client(app, client):
    user = User(id=1, display_name="Test User", role=Role.NINJA)
    with app.test_request_context():
        token = create_access_token(identity=user)
    client.environ_base["HTTP_AUTHORIZATION"] = "Bearer " + token
    return client


def scoped_route():
    pass


@pytest.mark.parametrize(
    "scope,code",
    [
        pytest.param(Role.STUDENT, 200),
        pytest.param(Role.NINJA, 200),
        pytest.param(Role.ADMIN, 403),
    ],
)
def test_scopes(scope, code, app, ninja_client):
    @scoped(scope)
    def scoped_route():
        return "Test"

    app.add_url_rule("/scoped", "scoped_route", scoped_route)

    with app.test_request_context():
        resp = ninja_client.get("/scoped")
        assert resp.status_code == code
