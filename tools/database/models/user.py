from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship
from tools.database import BASE

from tools.utils import Role


class User(BASE):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    email = Column(String(255))

    role = Column(Enum(Role, name="role"))

    first_name = Column(String(255))
    last_name = Column(String(255))
    class_year = Column(Integer)

    tools = relationship("ToolLevel", backref="user")
    trainings = relationship("Training", backref="user")
