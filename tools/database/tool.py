from sqlalchemy import *
from . import Base


class Tool(Base):
    __tablename__ = "tool"
    id = Column(Integer, primary_key=True)
    name = Column(String)
