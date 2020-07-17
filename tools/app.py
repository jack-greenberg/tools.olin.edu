from flask import Flask
from tools.config import DevelopmentConfig, ProductionConfig
from tools.routes import blueprints

"""
Tools.Olin.Edu
"""


def start_app(config):
    app = Flask(__name__)
    app.config.from_object(config)

    for bp in blueprints:
        app.register_blueprint(bp)

    return app


if __name__ == "__main__":
    app = start_app()
    app.run("0.0.0.0")
