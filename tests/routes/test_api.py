import json

from tests.conftest import mock_user, mock_tool, mock_training


def test_user_trainings(app, client, db_session):
    user = mock_user(1, db_session)
    tool = mock_tool(1, db_session)
    training = mock_training(1, tool, pre=None, db_session=db_session)

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
                                tool {
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
                    {"training": {"id": "%s" % training.id, "tool": {"id": "1"}}}
                ],
            }
        }
