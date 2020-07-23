import json


def test_new_user(app, client):
    new_user = """
        mutation newUser {
            addUser (name: "tester", role: STUDENT) {
                name
                role
            }
        }
    """

    with app.test_request_context():
        app.preprocess_request()
        response = client.post("/api/graphql", data={"query": new_user})
        assert response.status_code == 200

        response_body = json.loads(response.data)
        assert response_body == {
            "data": {"addUser": {"name": "tester", "role": "STUDENT"}}
        }


def test_query_user(app, client):
    new_user = """
        mutation newUser {
            addUser (name: "tester", role: STUDENT) {
                id
                name
                role
            }
        }
    """

    with app.test_request_context():
        app.preprocess_request()
        response = client.post("/api/graphql", data={"query": new_user})
        assert response.status_code == 200

        response_body = json.loads(response.data)

        id = json.loads(response.data)["data"]["addUser"]["id"]

        user_query = (
            """
        query userQuery {
            user (id: %s) {
                name
                role
            }
        }
        """
            % id
        )

        response = client.post("/api/graphql", data={"query": user_query})
        response_body = json.loads(response.data)
        assert response_body == {
            "data": {"user": {"name": "tester", "role": "STUDENT"}}
        }
