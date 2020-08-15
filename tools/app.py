import os
import logging

from flask import Flask, g, flash, jsonify

from tools.config import DevelopmentConfig, ProductionConfig
from tools.routes import blueprints
from tools.errors import AppException
from tools.database import Session
from tools.auth import AuthHandler
from tools.config import AZURE_ENABLED

"""
Tools.Olin.Edu
"""

logger = logging.getLogger(__name__)


class Application(Flask):
    auth = AuthHandler()


def make_app(config):
    app = Application(__name__)
    app.config.from_object(config)

    # Error handling
    @app.errorhandler(AppException)
    def catch_exception(error):
        error_dict = error.to_dict()

        if error.code >= 500:
            logger.exception(f"Internal exception: {error.to_dict()}")
        else:
            logger.info(f"{error.message}: {error.to_dict()}")

        flash(error.message)
        # TODO: replace with render_template for error page
        return jsonify(error_dict), error.code

    @app.before_request
    def before():
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


def build_app():
    if os.getenv("ENV") == "production":
        config = ProductionConfig
    else:
        config = DevelopmentConfig

    if not AZURE_ENABLED:
        logger.warning("Running without Azure")

    return make_app(config)


def run_app():
    app = build_app()
    app.run("0.0.0.0")


if __name__ == "__main__":
    run_app()
