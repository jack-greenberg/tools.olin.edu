from tests.conftest import mock_user, mock_tool, mock_training


def test_new_training(app, client, db_session):
    user = mock_user(1, db_session)

    resp = client.post(
        "/api/",
        data={
            "query": """
            mutation newTraining {
                addTraining (
                    tool: "Lathe",
                ) {
                    tool {
                        name
                        category {
                            name
                        }
                    }
                }
            }
        """
        },
    ).get_json()
