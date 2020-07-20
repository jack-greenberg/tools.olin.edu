from sqlalchemy import Column, Table, Integer, String, Enum, ForeignKey
from sqlalchemy.orm import relationship
from tools.database import BASE
from tools.database.tool import TrainingLevel

from tools.utils import Scope


user_tool = Table(
    "user_tool",
    BASE.metadata,
    Column("user_id", Integer, ForeignKey("user.id"), primary_key=True),
    Column("tool_level_id", Integer, ForeignKey("tool_level.id"), primary_key=True),
)


class User(BASE):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    email = Column(String(255))

    scope = Column(Enum(Scope, name="scope"))

    first_name = Column(String(255))
    last_name = Column(String(255))
    class_year = Column(Integer)

    #  tools_trained = relationship("ToolLevel", backref="user")
