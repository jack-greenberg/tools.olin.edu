import json

from flask import Flask, request, g

from tools.config import DevelopmentConfig
from tools.routes import blueprints
from tools.routes.errors import AppException
from tools.database import BASE, ENGINE, Session

"""
Tools.Olin.Edu
"""


def make_app(config):
    app = Flask(__name__)
    app.config.from_object(config)

    # Error handling
    @app.errorhandler(AppException)
    def catch_exception(error):
        error_dict = json.dumps(error.to_dict())
        return error_dict

    @app.before_request
    def before():
        if request.endpoint == "api.graphql":
            g.db_session = Session()

    @app.teardown_request
    def after(errors=None):
        db_session = getattr(g, "db_session", None)

        if db_session:
            if not errors:
                db_session.commit()
            else:
                db_session.rollback()
            db_session.close()

    # Register blueprints
    for bp in blueprints:
        app.register_blueprint(bp)

    return app


def start_app(config):
    app = make_app(config)

    app.logger.info("Starting app...")
    app.run("0.0.0.0")


if __name__ == "__main__":
    BASE.metadata.create_all(bind=ENGINE)
    app = start_app(DevelopmentConfig)
