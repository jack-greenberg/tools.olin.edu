from flask import Flask
from tools.routes import API, public

"""
Tools.Olin.Edu
"""


def start_app():
    app = Flask(__name__)
    app.register_blueprint(API)
    app.register_blueprint(public)
