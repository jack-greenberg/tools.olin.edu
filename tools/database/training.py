from sqlalchemy import *
from . import Base


class Training(Base):
    __tablename__ = "training"
    id = Column(Integer, primary_key=True)
