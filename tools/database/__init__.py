import re

from sqlalchemy import create_engine, cast
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import ARRAY

from tools.config import DATABASE_CONFIG

__all__ = ["ENGINE", "Session", "BASE"]

ENGINE = create_engine(URL(**DATABASE_CONFIG))

Session = sessionmaker(bind=ENGINE)

BASE = declarative_base()

scope_session = scoped_session(Session)
BASE.query = scope_session.query_property()


"""
class BaseQuery(object):
    first or 404
    get
    insert
    upsert
    delete
"""


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
