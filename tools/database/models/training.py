from sqlalchemy import Column, Integer, ForeignKey, String, Table
from sqlalchemy.orm import relationship
from tools.database import BASE


# Association Object for Trainings and Tools
training_tool = Table(
    "training_tool",
    BASE.metadata,
    Column("training_id", Integer, ForeignKey("training.id")),
    Column("tool_id", Integer, ForeignKey("tool.id")),
)


class Training(BASE):
    __tablename__ = "training"
    id = Column(Integer, primary_key=True)
    name = Column(String)

    tools = relationship("Tool", secondary=training_tool)

    prerequisite_id = Column(Integer, ForeignKey("training.id"), nullable=True)
    prerequisite = relationship("Training", remote_side=[id])
