from flask import Blueprint, request, current_app, session, redirect, url_for
from flask_graphql import GraphQLView

from tools.database.schemas import AppSchema

API = Blueprint("api", __name__, url_prefix="/api")

API.add_url_rule(
    "/", view_func=GraphQLView.as_view("graphql", schema=AppSchema, graphiql=True)
)

# CURRENTLY USED BUT NEEDS TO BE REPLACED
@API.route("/token")
def get_token():
    if request.args.get("state") != session.get("state"):
        return redirect(url_for("tools.index"))  # No-OP. Goes back to Index page
    if "error" in request.args:  # Authentication/Authorization failure
        return "Oh no!"

    if request.args.get("code"):
        response = current_app.auth.get_token(
            code=request.args.get("code"),
            scopes=["User.ReadBasic.All"],
            redirect_uri="http://localhost:8000/api/token",  # url_for("tools.index")
        )
        session["user"] = response.get("id_token_claims")
    # return redirect(url_for("tools.index"))
    return redirect("http://localhost:8000/api/token")
