from flask import Blueprint, request, current_app, session, url_for, redirect

from tools.errors import AppException

AUTH = Blueprint("auth", __name__, url_prefix="/auth")


class AuthException(AppException):
    pass


@AUTH.route("/token")
def get_token():
    if request.args.get("state") != session.get("state"):
        return redirect(url_for("tools.index"))  # No-op, goes back to Index page
    if "error" in request.args:
        raise AuthException(
            "There was an error in the auth process: {}".format(
                request.args.get("error")
            )
        )

    if request.args.get("code"):
        result = current_app.auth.get_token(
            code=request.args.get("code"),
            scopes=["User.ReadBasic.All"],
            # redirect_uri=url_for("tools.index"),
            redirect_uri="http://localhost:8000/api/token",
        )
        session["user"] = result.get("id_token_claims")
        session["token"] = result.get("access_token")
        session["refresh_token"] = result.get("refresh_token")
    # return redirect(url_for("tools.index"))
    return redirect("http://localhost:8000/api/token")
