from flask import Blueprint, g, request, current_app, session, url_for, redirect

from tools.errors import AuthException
from tools.database.models import User
from tools.utils import Role

AUTH = Blueprint("auth", __name__, url_prefix="/auth")


@AUTH.route("/token")
def get_token():
    if request.args.get("state") != session.get("state"):
        raise AuthException("Mismatched state", code=400)

    if "error" in request.args:
        raise AuthException(
            "Exception in auth process: {}".format(request.args.get("error")), code=500
        )

    if request.args.get("code"):
        token_data = current_app.auth.get_token(
            code=request.args.get("code"),
            scopes=["User.ReadBasic.All"],
            redirect_uri=url_for("auth.get_token", _external=True),
        )

        session["user"] = token_data.get("id_token_claims")
        session["access_token"] = token_data.get("access_token")
        session["refresh_token"] = token_data.get("refresh_token")

        current_user = current_app.auth.get_current_user()
        existing_user = (
            g.db_session.query(User)
            .filter_by(user_id=session["user"].get("oid"))
            .first()
        )

        # TODO: eventually replace with upsert
        if not existing_user:
            # INFO Log adding new user
            new_user = User(
                user_id=current_user.get("user_id"),
                email=current_user.get("email"),
                first_name=current_user.get("first_name"),
                last_name=current_user.get("last_name"),
                display_name=current_user.get("display_name"),
                role=Role.STUDENT,
            )
            g.db_session.add(new_user)
            g.db_session.flush()
        else:
            for key, value in current_user.items():
                setattr(existing_user, key, value)

        # This is authed, so could return to /dashboard or something
        return redirect(url_for("tools.index"))

    raise AuthException("No code provided", code=400)


@AUTH.route("/logout")
def logout():
    session.clear()
    return redirect(current_app.auth.get_logout_url())
