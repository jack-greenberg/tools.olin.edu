from sqlalchemy import Column, Integer
from tools.database import BASE


class Training(BASE):
    __tablename__ = "training"
    id = Column(Integer, primary_key=True)
