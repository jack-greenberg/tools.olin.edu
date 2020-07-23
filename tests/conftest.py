import pytest

from tools.app import make_app
from tools.config import ProductionConfig


@pytest.fixture
def app():
    app = make_app(ProductionConfig)
    app.config["TESTING"] = True
    return app


@pytest.fixture
def client(app):
    return app.test_client()
