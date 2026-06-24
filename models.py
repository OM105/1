from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime
from schema import TaskStatus, Priority

Base = declarative_base()

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key = True, index = True)
    title = Column(String)
    status = Column(Enum(TaskStatus), default = TaskStatus.pending)
    priority = Column(Enum(Priority), default = Priority.M)
    Description = Column(String, nullable=True)
    due_date = Column(DateTime, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default = datetime.now, nullable = False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)


    

class DBUser(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True, index = True)
    username = Column(String, unique = True)
    disabled = Column(Boolean, default=False)
    hashed_password = Column(String)