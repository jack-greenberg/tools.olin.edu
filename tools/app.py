import os
import json
import logging

from flask import Flask, g

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
        if error.code >= 500:
            logger.exception(f"Internal exception: {error.to_dict}")
        else:
            logger.info(f"{error.message}: {error.to_dict()}")

        error_dict = json.dumps(error.to_dict())
        return error_dict

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


if __name__ == "__main__":
    if os.getenv("ENV") == "production":
        config = ProductionConfig
    else:
        config = DevelopmentConfig

    if not AZURE_ENABLED:
        logger.warning("Running without Azure")

    app = make_app(config)
    app.run("0.0.0.0")
