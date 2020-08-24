import pytest
import uuid
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from flask import session, current_app
from flask_jwt_extended import create_access_token

from tools.app import make_app
from tools.utils import Role
from tools.config import ProductionConfig, DATABASE_CONFIG
from tools.database.models import User, Training, Tool, ToolCategory
from tools.database import Session, BASE


@pytest.fixture
def app():
    app = make_app(ProductionConfig)
    app.config["TESTING"] = True
    app.config["JWT_TOKEN_LOCATION"] = ["headers", "cookies"]

    def index():
        if not session.get("user"):
            state = str(uuid.uuid4())
            session["state"] = state
            login_url = current_app.auth.get_auth_url(state=state)
            return "<a href='{0}'>Click to log in</a>".format(login_url)

        return "Welcome {}!".format(session.get("user").get("name"))

    app.add_url_rule("/", "index", view_func=index)
    return app


@pytest.fixture
def client(app):
    user = User(id=1, display_name="Test User", role=Role.ADMIN)
    with app.test_request_context():
        token = create_access_token(identity=user)
    client = app.test_client()
    client.environ_base["HTTP_AUTHORIZATION"] = "Bearer " + token
    return client


@pytest.fixture
def current_user(app, client):
    with client.session_transaction() as sess:
        sess["user"] = {"oid": "some_user_id"}
    return


@pytest.fixture
def engine():
    engine = create_engine(URL(**DATABASE_CONFIG))

    yield engine

    engine.dispose()


@pytest.fixture
def db(engine):
    BASE.metadata.drop_all(bind=engine)
    BASE.metadata.create_all(bind=engine)

    yield

    BASE.metadata.drop_all(bind=engine)
    BASE.metadata.create_all(bind=engine)


@pytest.fixture
def db_session(db):
    session = Session()

    try:
        yield session
    finally:
        session.close()


def mock_user(id, db_session=None, **kwargs):
    u = User(id=id, **kwargs)
    db_session.add(u)
    db_session.flush()
    db_session.commit()
    return u


def mock_tool(id, db_session=None, **kwargs):
    category_name = kwargs.pop("category", None)

    t = Tool(id=id, **kwargs)
    if category_name:
        category = ToolCategory(name=category_name)
        t.category = category

    db_session.add(t)
    db_session.flush()
    db_session.commit()
    return t


def mock_training(id, db_session=None, tools=None, pre=None, **kwargs):
    tr = Training(id=id, **kwargs)
    tr.tools = tools

    if pre:
        tr.prerequisite = pre

    db_session.add(tr)
    db_session.flush()
    db_session.commit()
    return tr
