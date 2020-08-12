import pytest
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL

from tools.app import make_app
from tools.config import ProductionConfig, DATABASE_CONFIG
from tools.database.models import User, Training, Tool, ToolCategory
from tools.database import Session, BASE


@pytest.fixture
def app():
    app = make_app(ProductionConfig)
    app.config["TESTING"] = True
    return app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def engine():
    engine = create_engine(URL(**DATABASE_CONFIG))

    yield engine

    engine.dispose()


@pytest.fixture
def db(engine):
    BASE.metadata.create_all(bind=engine)

    yield

    BASE.metadata.drop_all(bind=engine)


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
