from sqlalchemy import Column, Integer, String, ForeignKey, Enum as EnumType
from tools.database import BASE, ArrayOfEnum
from enum import Enum


class TrainingLevel(Enum):
    BASIC = "Basic"
    INTERMEDIATE = "Intermediate"
    CNC = "CNC"


class Tool(BASE):
    __tablename__ = "tool"
    id = Column(Integer, primary_key=True)
    name = Column(String)


class ToolLevel(BASE):
    __tablename__ = "tool_level"
    id = Column(Integer, primary_key=True)
    tool_id = Column(Integer, ForeignKey("tool.id"))
    level = Column(EnumType(TrainingLevel))
