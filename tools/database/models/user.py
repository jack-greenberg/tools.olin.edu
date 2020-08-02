import enum

from sqlalchemy import Column, Integer, Enum, String, ForeignKey
from sqlalchemy.orm import relationship

from tools.database import BASE
from tools.utils import Role, TrainingStatus


class User(BASE):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    user_id = Column(String)
    email = Column(String(255))

    role = Column(Enum(Role, name="role"))

    display_name = Column(String(255))
    first_name = Column(String(255))
    last_name = Column(String(255))
    class_year = Column(Integer)

    trainings = relationship(
        "UserTraining", back_populates="user", innerjoin=True, lazy="select"
    )


class UserTraining(BASE):
    __tablename__ = "user_training"
    id = Column(Integer, primary_key=True)
    training_id = Column(Integer, ForeignKey("training.id"))
    training = relationship("Training")

    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="trainings")

    status = Column(Enum(TrainingStatus))
