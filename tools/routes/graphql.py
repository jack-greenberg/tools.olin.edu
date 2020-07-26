from flask import Blueprint, request, current_app, session, redirect, url_for, g
from flask_graphql import GraphQLView

from tools.database.schemas import AppSchema
from tools.database.models import User

from tools.utils import Role

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
        session["access_token"] = response.get("access_token")
        session["refresh_token"] = response.get("refresh_token")

        db_result = (
            g.db_session.query(User)
            .filter_by(user_id=session["user"].get("oid"))
            .first()
        )

        print(db_result)
        if not db_result:
            current_user = current_app.auth.get_current_user()

            new_user = User(
                user_id=current_user.get("id"),
                email=current_user.get("mail"),
                first_name=current_user.get("givenName"),
                last_name=current_user.get("surname"),
                role=Role.STUDENT,
            )
            g.db_session.add(new_user)
            g.db_session.flush()
    # return redirect(url_for("tools.index"))
    return redirect("http://localhost:8000/api/token")
