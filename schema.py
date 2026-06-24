from pydantic import BaseModel
from datetime import datetime
from enum import Enum

class TaskStatus(str, Enum):
    pending = "pending"
    in_progress = "in progress"
    completed = "completed"

class Priority(str, Enum):
    H = "H"
    M = "M"
    L = "L"

class TaskCreate(BaseModel):
    title: str
    status: TaskStatus
    priority: Priority | None
    Description: str | None
    due_date: datetime | None

class TaskResponse(BaseModel):
    id: int
    title: str 
    status: TaskStatus
    priority: Priority 
    Description: str | None
    due_date: datetime | None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class User(BaseModel):
    username: str
    disabled: bool

    
class UserRegister(BaseModel):
    username: str
    password: str
   

class UserResponse(BaseModel):
    id: int
    username: str
    disabled: bool

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None