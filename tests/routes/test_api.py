import pytest
import json

from tests.conftest import mock_user, mock_tool, mock_training
from tools.routes.graphql import error_formatter
from tools.errors import AppException


def test_user_trainings(app, client, db_session, current_user):
    user = mock_user(1, db_session)
    tool = mock_tool(1, db_session)
    training = mock_training(1, db_session=db_session, tools=[tool])

    with app.test_request_context():
        app.preprocess_request()

        response = client.post(
            "/api/",
            data={
                "query": """
                query {
                    user (id: %s) {
                        id
                        trainings {
                            id
                        }
                    }
                }
                """
                % (user.id)
            },
        )

        assert json.loads(response.data).get("data") == {
            "user": {"id": "1", "trainings": []}
        }

        response = client.post(
            "/api/",
            data={
                "query": """
                mutation {
                    addUserTraining (
                        userId: 1
                        trainingId: 1
                    ) {
                        id
                        trainings {
                            training {
                                id
                                tools {
                                    id
                                }
                            }
                        }
                    }
                }
                """
            },
        )

        data = json.loads(response.data)
        assert "errors" not in data
        assert data["data"] == {
            "addUserTraining": {
                "id": "1",
                "trainings": [
                    {"training": {"id": "%s" % training.id, "tools": [{"id": "1"}]}}
                ],
            }
        }


def test_update_user_training_status(client, app, db_session, current_user):
    mock_user(1, db_session)
    tool = mock_tool(1, db_session)
    mock_training(1, db_session, tools=[tool])

    with app.test_request_context():
        app.preprocess_request()

        response = client.post(
            "/api/",
            data={
                "query": """
                mutation {
                    addUserTraining (
                        userId: 1
                        trainingId: 1
                    ) {
                        id
                        trainings {
                            training {
                                id
                                tools {
                                    id
                                }
                            }
                        }
                    }
                }
                """
            },
        )

        assert response.status_code == 200
        assert "errors" not in json.loads(response.data)

        response = client.post(
            "/api/",
            data={
                "query": """
                mutation {
                    updateTrainingStatus (
                        userId: 1
                        trainingId: 1
                        status: COMPLETE
                    ) {
                        status
                    }
                }
                """
            },
        )

        data = json.loads(response.data)
        assert "errors" not in data
        assert data["data"] == {"updateTrainingStatus": {"status": "COMPLETE"}}


def test_api_errors(app, client, db_session, current_user):
    mock_user(1, db_session)

    with app.test_request_context():
        response = client.post(
            "/api/",
            data={
                "query": """
                    this will fail
                """
            },
        )
    assert response.status_code == 500


def test_error_formatter():
    err = AppException("Oh no :(", code=419)
    err.original_error = AppException("Something else", code=500)

    with pytest.raises(AppException) as raised:
        error_formatter(err)

    assert raised.value.message == "Something else"
