from database import get_db
from fastapi import APIRouter,HTTPException,Depends
from models import TodoRequest,TodoPatchRequest
import models
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/todos",
    tags = ["todos"]
)

@router.get("/todo/get-all")
async def get_all_todos(db:Session=Depends(get_db)):
    db_todo = db.query(models.Todos).all()
    return db_todo

@router.get("/todo/{todo_id}")
async def get_todo_by_id(todo_id:int,db:Session = Depends(get_db)):
    db_todo = db.query(models.Todos).filter(models.Todos.id.__eq__(todo_id)).first()
    if db_todo is None:
        raise HTTPException(status_code=404,detail="Todo Not Found")
    return db_todo

@router.post("/todo/create")
async def create_todo(todo:TodoRequest,db:Session=Depends(get_db)):
    db_todo = models.Todos(**todo.model_dump())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

@router.delete("/todo/delete/{todo_id}")
async def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(models.Todos).filter(models.Todos.id.__eq__(todo_id)).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(todo)
    db.commit()
    return {"message": "Todo deleted successfully"}

@router.patch("/todo/update/{id}")
async def update_todo(todo_id:int,todo_structure:TodoPatchRequest,db:Session=Depends(get_db)):
    todo = db.query(models.Todos).filter(models.Todos.id .__eq__(todo_id)).update(todo_structure.model_dump(exclude_unset=True))
    if todo == 0:
        raise HTTPException(status_code=404,detail="Todo Not Found")

    db.commit()
    return {"message": "Todo updated successfully"}
