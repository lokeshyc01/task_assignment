from pydantic import BaseModel,Field
from datetime import datetime

class TaskBase(BaseModel):
    title:str = Field(...,max_length=100)
    description:str = Field(max_length=255)
    duedate:datetime | None = None
    priority:str = Field(...,pattern="^(High|Medium|Low)$")  

class TaskUpdate(BaseModel):
    title:str | None = None
    description:str | None = None
    duedate : datetime | None = None
    priority:str = Field(pattern="^(High|Medium|Low)$")


class Task(TaskBase):
    id:int
    is_completed:bool

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    name:str = Field(...)

class UserCreate(UserBase):
    password:str = Field(...,min_length=5)

class User(UserBase):
    id:int
    tasks:list[Task] = []

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token:str
    token_type:str