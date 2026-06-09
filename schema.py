from pydantic import BaseModel

class TaskCreate(BaseModel):
    title: str
    status: str

class TaskResponse(BaseModel):
    id: int
    title: str 
    status: str
    
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