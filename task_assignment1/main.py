from fastapi import FastAPI,Depends,HTTPException
from pydantic import ValidationError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from . import model,schema,crud,utils
from .database import SessionLocal,engine
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from jose import JWTError, jwt

#model.Base.metadata.drop_all(bind=engine)

model.Base.metadata.create_all(bind=engine) #create the database and columns as per model
app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.exception_handler(ValidationError)
async def custom_validation_exception_handler(request,exc:ValidationError):
    print("validation error")
    return HTTPException(status_code=422, detail=exc.errors())

@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request,exc:HTTPException):
    return JSONResponse(status_code=exc.status_code,
                        content=jsonable_encoder({"details":exc.detail})
                        )

@app.get("/")
def say_hello():
    return "Jay Ganesh..."

async def get_current_user(token:Annotated[str , Depends(oauth2_scheme)]):
    try:
        user = utils.get_user(token)
    except:
        raise
    return user

@app.post("/tasks",response_model=schema.Task,status_code=201,dependencies=[Depends(get_current_user)])
async def create_taks(task:schema.TaskBase,db:Session = Depends(get_db)):
    try:
        return crud.create_task(db,task)
    except: 
        raise

@app.get("/tasks",response_model=list[schema.Task],status_code=200,dependencies=[Depends(get_current_user)])
async def get_tasks(is_completed:bool | None = None,priority:str | None = None,db:Session = Depends(get_db)):
    try:
        if is_completed is not None:
            return crud.get_all_tasks(db,is_completed=is_completed)
        elif priority is not None:
            return crud.get_all_tasks(db,priority=priority)
        else:
            return crud.get_all_tasks(db)
    except:
        raise

@app.get("/tasks/{task_id}",response_model=schema.Task,status_code=200,dependencies=[Depends(get_current_user)])
async def get_task(task_id:int,db:Session = Depends(get_db)):
    try:
        return crud.get_task_by_id(db,task_id)
    except:
        raise

@app.delete("/tasks/{task_id}",status_code=200,dependencies=[Depends(get_current_user)])
async def delete_task(task_id:int,db:Session = Depends(get_db)):
    try:
        crud.delete_task_by_id(db,task_id)
        return "task deleted"
    except:
        raise

@app.put("/tasks/{task_id}" , response_model=schema.Task,status_code=200,dependencies=[Depends(get_current_user)])
async def update_task(task_id:int,task:schema.TaskUpdate,db:Session = Depends(get_db)):
    try:
        return crud.update_task(db,task_id,task) 
    except:
        raise

@app.post("/users",status_code=201,response_model=schema.User)
async def create_user(user:schema.UserCreate,db:Session = Depends(get_db)):
    try:
        return crud.create_User(db,user)
    except:
        raise

@app.post("/users/{user_id}/items",response_model=schema.Task,dependencies=[Depends(get_current_user)],status_code=201)
async def create_task_for_user(user_id:int,task:schema.TaskBase,db:Session = Depends(get_db)):
    try:
        return crud.add_task_to_user(db,user_id,task)
    except:
        raise

@app.get("/users",response_model=list[schema.User],dependencies=[Depends(get_current_user)],status_code=200) #list of users need to define as we are getting list from db
async def get_users(db:Session = Depends(get_db)):
    try:
        return crud.get_all_users(db)
    except:
        raise

@app.post("/token")
async def login_for_access_token(formdata:Annotated[OAuth2PasswordRequestForm,Depends()],db:Session = Depends(get_db)):
    try:
        user = utils.authenticate_user(db,formdata.username,formdata.password)
        if not user:
            raise HTTPException(
                status_code=401,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expire = timedelta(minutes=30)
        token = utils.create_access_token(data = {"sub":user.name},expires_delta = access_token_expire)
        return schema.Token(access_token=token,token_type="bearer")
    except:
        raise