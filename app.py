from flask import Flask
from config import DevelopmentConfig, ProductionConfig

def create_app(config):
	app = Flask(__name__)
	app.config.from_object(config)

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
