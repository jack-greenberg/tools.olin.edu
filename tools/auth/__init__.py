from flask import session, current_app
from tools.errors import LoginRequired

from .azure import AuthHandler


def authed(f):
    def wrapped(*args, **kwargs):
        if not session.get("user"):
            raise LoginRequired(
                "This endpoint requires a login.",
                login_url=current_app.auth.get_auth_url(),
            )
        return f(*args, **kwargs)

    return wrapped


__all__ = ["AuthHandler", "authed"]
