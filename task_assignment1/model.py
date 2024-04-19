from sqlalchemy import Column,ForeignKey,Integer,String,Boolean,DateTime
from sqlalchemy.orm import relationship
from .database import Base

# 	id (int): Unique identifier for each task (auto-generated on creation)
# 	title (str): Title of the task (required, max length 100 characters)
# 	description (str): Optional description of the task (max length 255 characters)
# 	due_date (datetime): Date and time by which the task should be completed (optional)
# 	priority (str): Priority level of the task (e.g., "High", "Medium", "Low")
# 	is_completed (bool): Flag indicating whether the task is completed (default: False)


class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer,primary_key=True)
    title = Column(String(255))
    description = Column(String(255))
    duedate = Column(DateTime)
    priority = Column(String(255))
    is_completed = Column(Boolean,default=False)
    user_id = Column(Integer,ForeignKey("users.id"))

    user = relationship("User",back_populates="tasks")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True)
    name = Column(String(255),unique=True)
    password = Column(String(255))
    tasks = relationship("Task",back_populates="user")