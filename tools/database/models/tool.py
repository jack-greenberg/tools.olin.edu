from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from tools.database import BASE


class Tool(BASE):
    __tablename__ = "tool"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    category_id = Column(Integer, ForeignKey("tool_category.id"))
    category = relationship("ToolCategory", back_populates="tools")


class ToolCategory(BASE):
    __tablename__ = "tool_category"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    tools = relationship("Tool", back_populates="category")
