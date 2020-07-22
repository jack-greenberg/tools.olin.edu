from sqlalchemy import Column, Integer, String, ForeignKey, Enum as EnumType
from sqlalchemy.orm import relationship
from tools.database import BASE  # , ArrayOfEnum
from enum import Enum


class TrainingLevel(Enum):
    BASIC = "Basic"
    INTERMEDIATE = "Intermediate"
    CNC = "CNC"


class Tool(BASE):
    __tablename__ = "tool"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    levels = relationship("ToolLevel")
    category_id = Column(Integer, ForeignKey("tool_category.id"))
    category = relationship("ToolCategory", back_populates="tools")


class ToolCategory(BASE):
    __tablename__ = "tool_category"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    tools = relationship("Tool", back_populates="category")


class ToolLevel(BASE):
    __tablename__ = "tool_level"
    id = Column(Integer, primary_key=True)
    level = Column(EnumType(TrainingLevel))
    tool_id = Column(Integer, ForeignKey("tool.id"))
    prerequisite = Column(Integer, ForeignKey("tool_level.id"))
    postrequisite = relationship("ToolLevel")
