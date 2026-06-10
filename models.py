from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key = True, index = True)
    title = Column(String)
    status = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))

class DBUser(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key = True, index = True)
    username = Column(String, unique = True)
    disabled = Column(Boolean, default=False)
    hashed_password = Column(String)