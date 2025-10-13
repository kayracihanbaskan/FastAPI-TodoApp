from datetime import timedelta, datetime, timezone

from fastapi import APIRouter,Depends,HTTPException
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer

from passlib.context import CryptContext
from typing import Annotated

import models
from database import get_db
from sqlalchemy.orm import Session
from models import UserRequest, Token ,UserPatchRequest

from jose import jwt, JWTError

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

SECRET_KEY = 'cGTFMtOeXtzrJCBZ7MKLhthrWWWtx0cKAJSRf8o6cBV83CVTiTVG6bVaO9Wmv9jM'
REFRESH_SECRET_KEY = 'kCuKriXlCkU1vM2bixz6ow2A4OH8WQpu7LR0NW9RsPngodqtm4J3WetnA2zAZCEq'
ALGORITHM = 'HS256'

bcrypt_context = CryptContext(schemes=["bcrypt"],deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='token')

@router.post("/user/create/")
async def create_user(create_user_request:UserRequest,db:Session=Depends(get_db)):
    user = models.Users(
    username = create_user_request.username,
    name = create_user_request.name,
    surname = create_user_request.surname,
    email = create_user_request.email,
    hashed_password = bcrypt_context.hash(create_user_request.hashed_password),
    isActive = create_user_request.isActive,
    role = create_user_request.role
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def create_access_token(username:str,user_id:int,expires_delta:timedelta):
    encode = {
        'sub':username,
        'id':user_id,
        'type':'access',
        'iat':datetime.now(timezone.utc)
    }
    expire = datetime.now(timezone.utc) + expires_delta
    encode.update({"exp": expire})
    return jwt.encode(encode,SECRET_KEY,algorithm=ALGORITHM)

def create_refresh_token(username:str,user_id:int):
    encode = {
        'sub':username,
        'id':user_id,
        'type':'refresh',
        'iat':datetime.now(timezone.utc)
    }
    expire = datetime.now(timezone.utc) + timedelta(days=7)
    encode.update({"exp":expire})
    return jwt.encode(encode,REFRESH_SECRET_KEY,algorithm=ALGORITHM)

async def get_current_user( token : Annotated[str,Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
        username : str = payload.get("sub")
        user_id :int = payload.get('id')
        if username is None or user_id is None:
            raise HTTPException(status_code=401,detail="Could not validate user.")
        return {'username':username,"id":user_id}
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate user.")

@router.post("/user/login",response_model=Token)
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: Session = Depends(get_db)
):
    user = db.query(models.Users).filter_by(username=form_data.username).first()
    if not user or not bcrypt_context.verify(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="User or password is incorrect")
    token = create_access_token(user.username,user.id,timedelta(minutes=20))
    refresh_token = create_refresh_token(user.username,user.id
                                         )
    return {
        "access_token": token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.get("/user/all")
async def get_all_user(db:Session=Depends(get_db)):
    users = db.query(models.Users).filter().all()
    if users is None:
        raise HTTPException(status_code=404,detail="Db is empty")
    return users

@router.get("/user/{user_id}")
async def get_user_by_id(user_id:int,db:Session=Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id.__eq__(user_id)).first()
    if user is None:
        raise HTTPException(status_code=404,detail="User not found")
    return user

@router.delete("/user/delete/{user_id}")
async def delete_user_by_id(user_id:int,db:Session=Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id.__eq__(user_id)).first()
    if user is None:
        raise HTTPException(status_code=404,detail="User not found")
    db.delete(user)
    db.commit()
    return {"message":"User Deleted Successfully!"}

@router.patch("/user/update/{user_id}")
async def update_user_by_id(user_id:int,user_request:UserPatchRequest,db:Session=Depends(get_db)):
    user = db.query(models.Users).filter_by(id=user_id).update(user_request.model_dump(exclude_unset=True))
    if user is None:
        raise HTTPException(status_code=404,detail="User not found!")
    db.commit()
    user_get = db.query(models.Users).filter(models.Users.id.__eq__(user_id)).first()
    return {
        "message":"Updated Successfully",
        "user":user_get
    }


