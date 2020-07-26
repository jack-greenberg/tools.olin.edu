from sqlalchemy import Column, Integer, Enum, String
from tools.database import BASE

# from sqlalchemy.orm import relationship

from tools.utils import Role


class User(BASE):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    user_id = Column(String, primary_key=True)
    name = Column(String(255))
    email = Column(String(255))

    role = Column(Enum(Role, name="role"))

    first_name = Column(String(255))
    last_name = Column(String(255))
    class_year = Column(Integer)

    # trainings = relationship(
    #     "Training",
    #     back_populates="user",
    #     innerjoin=True,
    #     lazy="select"
    # )


class UserRole(BASE):
    __tablename__ = "user_role"
    user_id = Column(Integer, primary_key=True)
    role = Column(Enum(Role))


# class UserToolLevel(BASE):
#     __tablename__ = "user_tool_level"
#     user = relationship("User", back_populates="tools")
#     user_id = Column("user_id", Integer, ForeignKey("user.id"), primary_key=True)
#
#     tool_id = Column("tool_id", Integer, ForeignKey("tool.id"), primary_key=True)
#     tool_level = Column(Enum(TrainingLevel))
