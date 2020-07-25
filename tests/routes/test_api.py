import json
from unittest.mock import patch

from tools.auth import AuthHandler


def test_current_user(app, client):
    user_data = {
        "id": "cab20189-bf1d-479a-9d3e-37dc33b3b450",
        "mail": "Brian.Johnston@olin.edu",
        "displayName": "Brian Johnston",
        "givenName": "Brian",
        "surname": "bjohnston@olin.edu",
    }

    with patch.object(AuthHandler, "get_current_user", return_value=user_data):
        with app.test_request_context():
            app.preprocess_request()
            response = client.post(
                "/graphql/",
                data={
                    "query": """
                query {
                    user (
                        id: "cab20189-bf1d-479a-9d3e-37dc33b3b450"
                    ) {
                        id
                        mail
                        displayName
                        givenName
                        surname
                    }
                }
            """
                },
            )

            assert response.status_code == 200
            assert json.loads(response.data)["data"]["user"] == user_data
