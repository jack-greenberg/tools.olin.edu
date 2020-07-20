import pytest

#  from tools.database import create_session
from tools.database import BASE
from tools.config import DATABASE_CONFIG
from sqlalchemy.engine.url import URL
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


# Session = sessionmaker(bind=engine)


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


#  @pytest.fixture(scope="module")
#  def engine():
#  engine = create_engine(
#  URL(**DATABASE_CONFIG)
#  )
#  #  return engine
#  yield engine
#  BASE.metadata.drop_all(engine)
#  engine.dispose()


#  @pytest.fixture(scope="module")
#  def db_session():
#  session = create_session()
#  yield session
#
#  session.close()

#  with session_scope() as session:
#  yield session
#  @pytest.fixture(scope="module")
#  def engine():
#  engine = init_engine()
#  print(engine)
#  yield engine
#  BASE.metadata.drop_all(engine)
#
#  @pytest.fixture(scope="function")
#  def db_session(engine):
#  session = create_session(engine)
#
#  yield session
#
#  session.close()
