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


DATABASE_CONFIG = {
    "drivername": "postgresql",
    "host": "tools-db",
    "port": "5432",
    "username": "tools",
    "password": "development",
    "database": "tools",
}

AZURE_APPLICATION_ID = os.getenv("AZURE_APPLICATION_ID", None)
AZURE_TENANT_ID = os.getenv("AZURE_TENANT_ID", None)
AZURE_CLIENT_SECRET = os.getenv("AZURE_CLIENT_SECRET", None)
AZURE_AUTHORITY = (
    "https://login.microsoftonline.com/" + AZURE_TENANT_ID if AZURE_TENANT_ID else None
)
