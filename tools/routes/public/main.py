from flask import Blueprint

public = Blueprint("public", __name__, url_prefix="/")


@public.route("/")
def index():
    return "ASDF"
