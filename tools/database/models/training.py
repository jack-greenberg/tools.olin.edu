from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from tools.database import BASE


class Training(BASE):
    __tablename__ = "training"
    id = Column(Integer, primary_key=True)
    name = Column(String)

    tool_id = Column(Integer, ForeignKey("tool.id"))
    tool = relationship("Tool")

    prerequisite = Column(Integer, ForeignKey("training.id"), nullable=True)
    postrequisite = relationship("Training")
