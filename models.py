from typing import Optional
from database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from pydantic import BaseModel, Field, field_validator


class Todos(Base):
    __tablename__ = 'todos'

    id = Column(Integer,primary_key=True,index=True,autoincrement=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    isComplete = Column("complete",Boolean,default=False)
    owner_id = Column(Integer,ForeignKey("users.id"))

class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer,primary_key=True,unique=True,index=True,autoincrement=True)
    username = Column(String,unique=True)
    name = Column("first_name",String)
    surname = Column("last_name",String)
    email = Column(String,unique=True)
    hashed_password = Column(String)
    isActive = Column("is_active",Boolean,default=True)
    role = Column(String)
    phone_number = Column("phone",String)

    @field_validator("role")
    def role_lowercase(cls,v):
        return v.casefold()

class UserRequest(BaseModel):
    username:str = Field(...,min_length=4,max_length=10,description="Username")
    name:str = Field(...,min_length=3,max_length=20,description="Name")
    surname :str = Field(...,min_length=2,max_length=20,description="Surname")
    email : str = Field(...,min_length=2,max_length=20,description="E-Mail")
    hashed_password :str
    isActive : bool
    role : str

class UserPatchRequest(BaseModel):
    name: Optional[str]
    surname :Optional[str]
    isActive : Optional[bool]
    role : Optional[str]
    phone_number : Optional[str]

class UserChangePasswordRequestModel(BaseModel):
    old_password : Optional[str]
    new_password : Optional[str]
    confirm_password : Optional[str]

class Token(BaseModel):
    access_token : str
    refresh_token :str
    token_type :str

class TodoResponse:
    id:int
    title:str
    description:str
    priority:int
    isComplete:bool

    class Config:
        orm_mode = True


class TodoRequest(BaseModel):
    title : str = Field(...,min_length=4,max_length=20,description="Todo Title")
    description : str = Field(...,min_length=5,description="Todo Description")
    priority : int = Field(...,gt=0,description="Todo Priority")
    isComplete : bool = Field(default=False,description="Todo Completion")
    owner_id : int = Field(...,gt=0,description="User ID")

class TodoPatchRequest(BaseModel):
    title : Optional[str] = Field(...,min_length=4,max_length=20,description="Todo Title")
    description : Optional[str] = Field(...,min_length=5,description="Todo Description")
    priority : Optional[int] = Field(...,gt=0,description="Todo Priority")
    isComplete : Optional[bool] = None