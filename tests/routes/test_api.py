import pytest

from tools.app import start_app
from tools.config import DevelopmentConfig
from tools.utils import Role

import json


@pytest.fixture
def client(db_session):
    app = start_app(DevelopmentConfig)
    app.config["TESTING"] = True
    return app.test_client()


def test_new_user(client):
    new_user = """
        mutation newUser {
            addUser (name: "tester", role: STUDENT) {
                id
                name
                role
            }
        }
    """

    response = client.post("/api/graphql", data={"query": new_user})
    assert response.status_code == 200

    response_body = json.loads(response.data)
    assert response_body["data"]["addUser"]["name"] == "tester"
    assert Role(response_body["data"]["addUser"]["role"].lower()) == Role.STUDENT


def test_query_user(client):
    new_user = """
        mutation newUser {
            addUser (name: "tester", role: STUDENT) {
                id
                name
                role
            }
        }
    """

    response = client.post("/api/graphql", data={"query": new_user})
    id = json.loads(response.data)["data"]["addUser"]["id"]
    assert response.status_code == 200

    user_query = (
        """
    query userQuery {
        user (id: %s) {
            name
        }
    }
    """
        % id
    )

    response = client.post("/api/graphql", data={"query": user_query})
    response = json.loads(response.data)["data"]["user"]

    assert response["name"] == "tester"
