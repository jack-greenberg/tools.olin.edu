from sqlalchemy import Column, Integer, String
from . import Base


class Tool(Base):
    __tablename__ = "tool"
    id = Column(Integer, primary_key=True)
    name = Column(String)
