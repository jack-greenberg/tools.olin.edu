import re

from sqlalchemy import create_engine, cast
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import ARRAY

from tools.config import DATABASE_CONFIG

BASE = declarative_base()

engine = create_engine(URL(**DATABASE_CONFIG))
db_session = sessionmaker(bind=engine)


# def db_connect(**kwargs):
#     """
#     Create database connection, should only happen once per application
#     """
#     engine = create_engine(
#         URL(**DATABASE_CONFIG),
#         **kwargs
#     )
#     BASE.metadata.create_all(bind=engine)
#     return engine
#
#
#  class SessionFactory(object):
#  """
#  A session maker, ensures that a sessionmaker is only created once
#  """
#  _pool = None
#  _sessionfactory = None
#
#  @classmethod
#  def session(cls, **kwargs):
#  if cls._sessionfactory is None:
#  engine = db_connect(**kwargs)
#  cls._pool = engine.pool
#  cls._sessionfactory = sessionmaker(
#  autocommit=False,
#  bind=engine
#  )
#  return cls._sessionfactory()


#  def create_session(**kwargs):
#  return SessionFactory.session(**kwargs)


class ArrayOfEnum(ARRAY):
    def bind_expression(self, bindvalue):
        return cast(bindvalue, self)

    def result_processor(self, dialect, coltype):
        super_rp = super(ArrayOfEnum, self).result_processor(dialect, coltype)

        def handle_raw_string(value):
            inner = re.match(r"^{(.*)}$", value).group(1)
            return inner.split(",") if inner else []

        def process(value):
            if value is None:
                return None
            return super_rp(handle_raw_string(value))

        return process
