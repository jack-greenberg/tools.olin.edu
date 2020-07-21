from flask import Blueprint

from flask_graphql import GraphQLView

from tools.database.schema import Schema

API = Blueprint("api", __name__, url_prefix="/api")

API.add_url_rule(
    "/graphql", view_func=GraphQLView.as_view("graphql", schema=Schema, graphiql=True)
)
