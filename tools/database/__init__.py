import re

from sqlalchemy import create_engine, cast
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import ARRAY

from tools.config import DATABASE_CONFIG
from tools.routes.errors import AppException

BASE = declarative_base()


class Base(BASE):
    """
    Base model object with added classes
    """

    pass
    #
    # # Create
    # @classmethod
    # @db_context
    # def new(cls, db_session=None, **kwargs):
    #     obj = cls(**kwargs)
    #     db_session.add(cls(obj))
    #     return obj
    #
    # # Read
    # @classmethod
    # @db_context
    # def all(cls, db_session=None, **kwargs):
    #     results = db_session.query(cls).all()
    #     return [r for r in results]
    #
    # @classmethod
    # @db_context
    # def find(cls, db_session=None, **kwargs):
    # result = db_session.query(cls).filter()
    #
    # # Update
    # @classmethod
    # @db_context
    # def update()


ENGINE = create_engine(URL(**DATABASE_CONFIG))

Session = sessionmaker(bind=ENGINE)


def db_context(f):
    def wrapper(*args, **kwargs):
        if kwargs.get("db_session"):
            return f(*args, **kwargs)

        db_session = Session()
        try:
            kwargs["db_session"] = db_session
            f(*args, **kwargs)
            db_session.commit()
        except Exception as e:
            db_session.rollback()
            raise AppException(e)
        finally:
            try:
                db_session.close()
            except:  # noqa
                print("Could not close session: %s" % db_session)

    return wrapper


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
# class SessionFactory(object):
#     """
#     A session maker, ensures that a sessionmaker is only created once
#     """
#     _pool = None
#     _sessionfactory = None
#
#     @classmethod
#     def session(cls):
#         if cls._sessionfactory is None:
#             engine = db_connect()
#             cls._pool = engine.pool
#             cls._sessionfactory = sessionmaker(
#                autocommit=False,
#                bind=engine
#             )
#         return cls._sessionfactory()


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
