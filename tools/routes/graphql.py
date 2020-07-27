from flask import Blueprint
from flask_graphql import GraphQLView

from tools.database.schemas import AppSchema

API = Blueprint("api", __name__, url_prefix="/api")

API.add_url_rule(
    "/", view_func=GraphQLView.as_view("graphql", schema=AppSchema, graphiql=True)
)
