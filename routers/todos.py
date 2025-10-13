from typing import Annotated

from database import get_db
from fastapi import APIRouter,HTTPException,Depends
from models import TodoRequest,TodoPatchRequest
import models
from sqlalchemy.orm import Session
from .auth import get_current_user

router = APIRouter(
    prefix="/todos",
    tags = ["todos"]
)

user_dependency = Annotated[dict,Depends(get_current_user)]

@router.get("/todo/get-all")
async def get_all_todos(user:user_dependency,db:Session=Depends(get_db)):
    db_todo = db.query(models.Todos).filter(models.Todos.owner_id.__eq__(user.get('id'))).all()
    return db_todo

@router.get("/todo/{todo_id}")
async def get_todo_by_id(user:user_dependency,todo_id:int,db:Session = Depends(get_db)):
    db_todo = db.query(models.Todos).filter(models.Todos.id.__eq__(todo_id) and models.Todos.owner_id.__eq__(user.get('id'))).first()
    if db_todo is None:
        raise HTTPException(status_code=404,detail="Todo Not Found")
    return db_todo

@router.post("/todo/create")
async def create_todo(user:user_dependency,todo:TodoRequest,db:Session=Depends(get_db)):
    if user is None:
        raise HTTPException(status_code=401,detail="Authentication failed")
    db_todo = models.Todos(**todo.model_dump())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

@router.delete("/todo/delete/{todo_id}")
async def delete_todo(user:user_dependency,todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(models.Todos).filter(models.Todos.id.__eq__(todo_id) and models.Todos.owner_id.__eq__(user.get('id'))).first()
    if not todo and user.get('role').__ne__('Admin'):
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(todo)
    db.commit()
    return {"message": "Todo deleted successfully"}

@router.patch("/todo/update/{id}")
async def update_todo(user:user_dependency,todo_id:int,todo_structure:TodoPatchRequest,db:Session=Depends(get_db)):
    todo = db.query(models.Todos).filter(models.Todos.id .__eq__(todo_id) and models.Todos.owner_id.__eq__(user.get('id'))).update(todo_structure.model_dump(exclude_unset=True))
    if todo == 0:
        raise HTTPException(status_code=404,detail="Todo Not Found")

    db.commit()
    return {"message": "Todo updated successfully"}
