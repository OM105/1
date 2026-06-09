from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schema import TaskCreate, TaskResponse, UserRegister, UserResponse
from database import get_db
import models
from typing import Annotated
from auth import *
from fastapi.security import OAuth2PasswordRequestForm



app = FastAPI()

@app.get("/users/me/items/")
async def read_own_items(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return [{"item_id": "Foo", "owner": current_user.username}]


@app.get("/users/me/")
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> User:
    return current_user

@app.post("/register", response_model = UserResponse)
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    existing_user = db.query(models.DBUser).filter(models.DBUser.username == user_data.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail = "User already exists")
    hash_pwd = hash_password(user_data.password)

    new_user = models.DBUser(
        username = user_data.username,
        hashed_password = hash_pwd,
        disabled = False
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/token")
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)) -> Token:
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Unauthorized user",
            headers = {"WWW-authenticate": "Bearer"}
        )

    ex = timedelta(minutes=30)
    access_token = create_token(data = {"sub": user.username}, expires_delta=ex)
    return Token(access_token = access_token, token_type = "bearer")

@app.get("/")
def root():
    return "Server is Running."

@app.get("/tasks", response_model = list[TaskResponse])
def get_tasks(db:Session = Depends(get_db)):
    tasks = db.query(models.Task).all()
    return tasks

@app.post("/tasks", response_model=TaskResponse)
def create_task1(task:TaskCreate, db:Session = Depends(get_db)):
    new_task = models.Task(title=task.title, status=task.status)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@app.get("/tasks/{task_id}", response_model = TaskResponse)
def get_task(task_id:int, db:Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()

    if task is None:
        raise HTTPException(status_code = 404, detail = "Task Not Found")

    return task

@app.delete("/tasks/{task_id}")
def del_task(task_id:int, db:Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    
    if task is None:
         raise HTTPException(status_code = 404, detail = "Task Not Found")
    else:
        db.delete(task)
        db.commit()
        return {"message": "Task Deleted Successfully"}
    
@app.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id:int, newdata:TaskCreate, db:Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    
    if task is None:
        raise HTTPException(status_code = 404, detail = "Task Not Found")
    
    task.title = newdata.title
    task.status = newdata.status
    db.commit()
    db.refresh(task)
    return task

@app.get("/tasks/{task_id}/toggle", response_model = TaskResponse)
def toggle(task_id:int, db:Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()

    if task is None:
        raise HTTPException(status_code = 404, detail = "Task Not Found")

    if task.status == "pending":
        task.status = "Done"
    else:
        task.status = "pending"
    
    db.commit()
    return task

@app.put("/tasks/{task_id}/{new_name}/change_title", response_model = TaskResponse)
def change_title(task_id: int, new_name: str, db:Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()

    if task is None:
        raise HTTPException(status_code = 404, detail = "Task Not Found")
    else:
        task.title = new_name
    
    db.commit()
    return task
