from flask import Flask
from flask import jsonify
from tools.config import DevelopmentConfig
from tools.routes import blueprints
from tools.routes.errors import AppException

"""
Tools.Olin.Edu
"""


def start_app(config):
    app = Flask(__name__)
    app.config.from_object(config)

    # Error handling
    @app.errorhandler(AppException)
    def catch_exception(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    # Register blueprints
    for bp in blueprints:
        app.register_blueprint(bp)

    return app


if __name__ == "__main__":
    app = start_app(DevelopmentConfig)
    app.logger.info("Starting app...")
    app.run("0.0.0.0")
