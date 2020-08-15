from flask import Blueprint
from flask_graphql import GraphQLView

from tools.database.schemas import AppSchema
from tools.auth import authed

API = Blueprint("api", __name__, url_prefix="/api")


class GraphQL(GraphQLView):
    decorators = [authed]


API.add_url_rule(
    "/", view_func=GraphQL.as_view("graphql", schema=AppSchema, graphiql=True)
)
