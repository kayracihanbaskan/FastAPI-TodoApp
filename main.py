from fastapi import FastAPI
from routers import auth, todos
import models
from models import Base
from database import engine

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/healthy/")
def check_health():
    return {'status':'Healthy'}

app.include_router(auth.router)
app.include_router(todos.router)
