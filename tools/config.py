"""
Configurations
"""
import os


class BaseConfig(object):
    TEMPLATES_AUTO_RELOAD = False
    JWT_TOKEN_LOCATION = ["headers"]
    JWT_ACCESS_COOKIE_PATH = "/auth/refresh"
    JWT_COOKIE_CSRF_PROTECT = False


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    ENV = "development"
    SECRET_KEY = "dev"


class ProductionConfig(BaseConfig):
    DEBUG = False
    TESTING = False
    ENV = "production"
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY", os.urandom(16))
