from flask import Blueprint
from flask_graphql import GraphQLView

from tools.database.schemas import AppSchema
from tools.errors import AppException
from tools.auth import authed

API = Blueprint("api", __name__, url_prefix="/api")


def error_formatter(e):
    if not hasattr(e, "original_error"):
        raise AppException(e.message)
    raise e.original_error


class GraphQL(GraphQLView):
    decorators = [authed]


API.add_url_rule(
    "/",
    "graphql",
    view_func=GraphQL.as_view(
        "graphql", schema=AppSchema, graphiql=True, format_error=error_formatter
    ),
)
