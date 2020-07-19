from flask import Blueprint

#  from flask_graphql import GraphQLView

# from tools.database import schema

API = Blueprint("api", __name__, url_prefix="/api")

# API.add_url_rule(
#     "/graphql",
#     view_func=GraphQLView.as_view(
#         "graphql",
#         schema=schema,
#         graphiql=True
#     )
# )
