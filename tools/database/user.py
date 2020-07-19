from sqlalchemy import Column, Integer, String, relationship
from . import Base

#  from tools.utils import Scope


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    email = Column(String(255))

    scopes = relationship("UserScope", lazy="selectin")

    first_name = Column(String(255))
    last_name = Column(String(255))

    # tools =
    # trainings =
