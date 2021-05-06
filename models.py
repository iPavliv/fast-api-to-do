from sqlalchemy import Column, String, Boolean, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Task(Base):
    __tablename__ = "Task"

    id = Column(Integer, primary_key=True)
    desc = Column(String)
    completed = Column(Boolean, default=False)
    list_id = Column(Integer, ForeignKey('TaskList.id', ondelete='CASCADE'))


class TaskList(Base):
    __tablename__ = "TaskList"

    id = Column(Integer, primary_key=True)
    desc = Column(String)
    tasks = relationship("Task", lazy="joined")
