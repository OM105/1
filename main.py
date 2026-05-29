from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from schema import TaskCreate, TaskResponse
from database import get_db
import models


app = FastAPI()


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

@app.put("/tasks/{task_id}/change_title", response_model = TaskResponse)
def change_title(task_id: int, db:Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()

    if task is None:
        raise HTTPException(status_code = 404, detail = "Task Not Found")
    else:
        task.title = "Renamed"
    
    db.commit()
    return task
