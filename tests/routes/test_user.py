import json

from tests.conftest import mock_user
from tools.utils import Role


def test_current_user(app, client, db_session):
    mock_user(1, db_session, user_id="my_user_id", email="alovelace@olin.edu")

    with client.session_transaction() as sess:
        sess["user"] = {"oid": "my_user_id", "name": "Ada Lovelace"}

    with app.test_request_context():
        resp = client.post(
            "/api/",
            data={
                "query": """
                query whoami {
                    me {
                        id
                        userId
                        email
                    }
                }
            """
            },
        )

        assert {
            "data": {
                "me": {"id": "1", "userId": "my_user_id", "email": "alovelace@olin.edu"}
            }
        } == json.loads(resp.data)


def test_get_a_user(app, client, db_session):
    mock_user(1, db_session, user_id="a_user_id")

    with app.test_request_context():
        resp = client.post(
            "/api/",
            data={
                "query": """
                query {
                    user (
                        id: 1
                    ) {
                        userId
                    }
                }
            """
            },
        )

        assert {"data": {"user": {"userId": "a_user_id"}}} == json.loads(resp.data)


def test_get_all_users(app, client, db_session):
    mock_user(1, db_session, user_id="user_id_1")
    mock_user(2, db_session, user_id="user_id_2")
    mock_user(3, db_session, user_id="user_id_3")

    with app.test_request_context():
        resp = client.post(
            "/api/",
            data={
                "query": """
                query {
                    users {
                        userId
                    }
                }
            """
            },
        )

        assert {
            "data": {
                "users": [
                    {"userId": "user_id_1"},
                    {"userId": "user_id_2"},
                    {"userId": "user_id_3"},
                ]
            }
        } == json.loads(resp.data)


def test_update_user_role(app, client, db_session):
    mock_user(1, db_session, user_id="a_user_id", role=Role.STUDENT)

    with app.test_request_context():
        resp = client.post(
            "/api/",
            data={
                "query": """
                mutation {
                    updateUserRole (
                        id: 1,
                        role: NINJA
                    ) {
                        userId
                        role
                    }
                }
            """
            },
        )

        assert {
            "data": {"updateUserRole": {"userId": "a_user_id", "role": "NINJA"}}
        } == json.loads(resp.data)
