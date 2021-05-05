from sqlalchemy import Column, String, Boolean, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Task(Base):
    __tablename__ = "Task"

    id = Column(Integer, primary_key=True)
    desc = Column(String)
    completed = Column(Boolean, default=False)
