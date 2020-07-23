from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from tools.database import BASE


class Training(BASE):
    __tablename__ = "training"
    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User")

    tool_id = Column(Integer, ForeignKey("tool.id"))
    tool = relationship("Tool")
