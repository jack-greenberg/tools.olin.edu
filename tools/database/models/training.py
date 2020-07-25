from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from tools.database import BASE


class Training(BASE):
    __tablename__ = "training"
    id = Column(Integer, primary_key=True)
    name = Column(String)

    # user_id = Column(Integer, ForeignKey("user.id"))
    # user = relationship("User", back_populates="trainings")
    # tool_level_id = Column(Integer, ForeignKey("tool_level.id"))
    # tool_level = relationship("ToolLevel")

    prerequisite = Column(Integer, ForeignKey("training.id"), nullable=True)
    postrequisite = relationship("Training")
