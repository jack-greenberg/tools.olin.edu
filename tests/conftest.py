import pytest

#  from tools.database import create_session
from tools.database import BASE
from tools.config import DATABASE_CONFIG
from sqlalchemy.engine.url import URL
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


@pytest.fixture(scope="session")
def engine():
    _engine = create_engine(URL(**DATABASE_CONFIG))

    yield _engine

    _engine.dispose()


@pytest.fixture(scope="function")
def db_session(engine):
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = Session()
    BASE.metadata.create_all(bind=engine)

    yield session

    session.rollback()
    session.close()
