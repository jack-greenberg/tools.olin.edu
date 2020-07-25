import uuid

from flask import Blueprint, session, current_app

tools = Blueprint("tools", __name__, url_prefix="/")


@tools.route("/")
def index():
    if not session.get("user"):
        state = str(uuid.uuid4())
        session["state"] = state
        login_url = current_app.auth.get_auth_url(state=state)
        return "<a href='{0}'>Click to log in</a>".format(login_url)

    return "Welcome {}!".format(session.get("user").get("name"))
