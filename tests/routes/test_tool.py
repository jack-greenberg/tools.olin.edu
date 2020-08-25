from tests.conftest import mock_tool
from tools.database.models import Tool, ToolCategory


def test_tool_queries(app, client, db_session, current_user):
    with app.test_request_context():
        resp = client.post(
            "/api/",
            data={
                "query": """
                mutation newTool {
                    addTool (
                        name: "Lathe",
                        category: "MetalWorking",
                    ) {
                        id,
                        name,
                        category {
                            name
                        }
                    }
                }
            """
            },
        )

        assert resp.status_code == 200
        assert {
            "data": {
                "addTool": {
                    "id": "1",
                    "name": "Lathe",
                    "category": {"name": "MetalWorking"},
                }
            }
        } == resp.get_json()

        tool_id = resp.get_json()["data"]["addTool"].get("id")
        tool_category = resp.get_json()["data"]["addTool"].get("category")["name"]
        assert db_session.query(Tool).filter_by(id=tool_id).first().name == "Lathe"
        assert (
            db_session.query(ToolCategory).filter_by(name=tool_category).first().name
            == "MetalWorking"
        )

        resp = client.post(
            "/api/",
            data={
                "query": """
                query getTool {
                    tool (
                        id: 1
                    ) {
                        name
                        category {
                            name
                        }
                    }
                }
            """
            },
        ).get_json()

        assert resp["data"]["tool"].get("name") == "Lathe"
        assert resp["data"]["tool"].get("category")["name"] == "MetalWorking"

        # This will test to make sure there are no errors when a category already exists
        client.post(
            "/api/",
            data={
                "query": """
                mutation newTool {
                    addTool (
                        name: "Mill",
                        category: "MetalWorking",
                    ) {
                        id,
                        name,
                        category {
                            name
                        }
                    }
                }
            """
            },
        )
        mock_tool(3, db_session, name="MIG Welder", category="Welding")

        resp = client.post(
            "/api/",
            data={
                "query": """
                query allTools {
                    tools {
                        name
                        category {
                            name
                        }
                    }
                }
            """
            },
        ).get_json()

        assert resp["data"]["tools"] == [
            {"name": "Lathe", "category": {"name": "MetalWorking"}},
            {"name": "Mill", "category": {"name": "MetalWorking"}},
            {"name": "MIG Welder", "category": {"name": "Welding"}},
        ]


def test_tools_by_category(app, client, db_session, current_user):
    mock_tool(1, db_session, name="Lathe", category="MetalWorking")
    mock_tool(2, db_session, name="Mill", category="MetalWorking")
    mock_tool(3, db_session, name="MIG Welder", category="Welding")

    with app.test_request_context():
        resp = client.post(
            "/api/",
            data={
                "query": """
                query metalWorkingTools {
                    toolsByCategory (
                        category: "MetalWorking"
                    ) {
                        name
                    }
                }
            """
            },
        ).get_json()["data"]

        assert [{"name": "Lathe"}, {"name": "Mill"}] == resp["toolsByCategory"]
