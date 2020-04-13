from flask import Flask
from config import DevelopmentConfig, ProductionConfig
from modules.db import db

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)

    with open("private/db_password") as f:
        password = f.read().rstrip()

    db_config = {
        'username': 'jackg',
        'password': password,
        'ip': '192.168.86.75',
        'database': 'tools'
    }

    app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql://{db_config['username']}:{db_config['password']}@{db_config['ip']}:3306/{db_config['database']}"
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
