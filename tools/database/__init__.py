from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base

from tools.config import DATABASE_CONFIG

__all__ = ["ENGINE", "Session", "BASE"]

ENGINE = create_engine(URL(**DATABASE_CONFIG))

Session = sessionmaker(bind=ENGINE)

BASE = declarative_base()

"""
class BaseQuery(object):
    first or 404
    get
    insert
    upsert
    delete
"""
