from flask import Flask
from config import DevelopmentConfig, ProductionConfig
from modules.db import db

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)

    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://jackg:eminem answered primarily charity@10.0.1.11:3306/tools"
    #  app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://tools.olin:Pursuit harvard pepper3;:jgreenberg-dev.olin.edu:3306"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    # Set up JSON Web Token (JWT) Authentication
    from flask_jwt_extended import JWTManager
    jwt = JWTManager(app)

    # Set up blueprints
    from blueprints.public import public
    app.register_blueprint(public)

    return app

app = create_app(DevelopmentConfig)

if __name__ == '__main__':
    app.run('0.0.0.0')
