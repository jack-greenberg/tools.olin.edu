from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker, relationship, backref

engine = create_engine("postgresql:///tools", convert_unicode=True)
db = scoped_session(session_maker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = db.query_property()
