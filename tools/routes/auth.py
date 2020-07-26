from flask import Blueprint, g, request, current_app, session, url_for, redirect

from tools.errors import AuthException
from tools.database.models import User
from tools.utils import Role

AUTH = Blueprint("auth", __name__, url_prefix="/auth")


@AUTH.route("/token")
def get_token():
    if request.args.get("state") != session.get("state"):
        return redirect(url_for("tools.index"))  # No-op, goes back to Index page

    if "error" in request.args:
        raise AuthException(
            "Exception in auth process: {}".format(request.args.get("error"))
        )

    if request.args.get("code"):
        result = current_app.auth.get_token(
            code=request.args.get("code"),
            scopes=["User.ReadBasic.All"],
            redirect_uri="http://localhost:8000/api/token",  # url_for("tools.index"),
        )

        session["user"] = result.get("id_token_claims")
        session["access_token"] = result.get("access_token")
        session["refresh_token"] = result.get("refresh_token")

        db_result = g.db_session.query(User).filter_by(
            user_id=session["user"].get("id")
        )

        if not db_result:
            current_user = current_app.auth.get_current_user()

            new_user = User(
                user_id=current_user.get("id"),
                email=current_user.get("email"),
                first_name=current_user.get("givenName"),
                last_name=current_user.get("surname"),
                role=Role.STUDENT,
            )
            g.db_session.add(new_user)
            g.db_session.flush()

    return redirect(
        "http://localhost:8000/api/token"
    )  # redirect(url_for("tools.index"))


@AUTH.route("/logout")
def logout():
    session.clear()
    return redirect(current_app.auth.get_logout_url())
