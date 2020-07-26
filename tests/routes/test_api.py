#  import json
#  from unittest.mock import patch
#
#  from tools.auth import AuthHandler
#
#
#  def test_current_user(app, client):
#  user_data = {
#  "id": "cab20189-bf1d-479a-9d3e-37dc33b3b450",
#  "mail": "Brian.Johnston@olin.edu",
#  "first_name": "Brian",
#  "last_name": "Johnston",
#  }
#
#  with patch("requests.get", return_value=user_data):
#  with app.test_request_context():
#  app.preprocess_request()
#  response = client.post(
#  "/api/",
#  data={
#  "query": """
#  query {
#  user (
#  id: "cab20189-bf1d-479a-9d3e-37dc33b3b450"
#  ) {
#  id
#  mail
#  firstName
#  lastName
#  }
#  }
#  """
#  },
#  )
#  print(response.data)
#
#  assert response.status_code == 200
#  assert json.loads(response.data)["data"]["user"] == user_data
