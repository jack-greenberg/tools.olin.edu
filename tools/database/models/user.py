from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from sqlalchemy.orm import relationship
from tools.database import BASE

from tools.utils import Role
from .tool import TrainingLevel


class User(BASE):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    email = Column(String(255))

    role = Column(Enum(Role, name="role"))

    first_name = Column(String(255))
    last_name = Column(String(255))
    class_year = Column(Integer)

    tools = relationship(
        "UserToolLevel", back_populates="user", innerjoin=True, lazy="select"
    )
    # trainings = relationship(
    #     "Training",
    #     backref="user",
    #     innerjoin=True,
    #     lazy="select",
    #     secondary=user_tool_level,
    #     back_populates=""
    # )


class UserToolLevel(BASE):
    __tablename__ = "user_tool_level"
    user_id = Column("user_id", Integer, ForeignKey("user.id"), primary_key=True)
    user = relationship("User", back_populates="tools")

    tool_id = Column("tool_id", Integer, ForeignKey("tool.id"), primary_key=True)

    tool_level = Column(Enum(TrainingLevel))
