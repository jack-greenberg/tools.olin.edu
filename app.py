from flask import Flask
from config import DevelopmentConfig, ProductionConfig
from modules.db import db
from blueprints.public import public
from blueprints.admin import admin

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)

    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///jgreenberg"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    with app.app_context():
        db.init_app(app)
        db.create_all()

    # Set up JSON Web Token (JWT) Authentication
    from flask_jwt_extended import JWTManager
    jwt = JWTManager(app)

    # Set up blueprints
    app.register_blueprint(public)
    app.register_blueprint(admin)

    return app

app = create_app(DevelopmentConfig)

if __name__ == '__main__':
    app.run('0.0.0.0')
