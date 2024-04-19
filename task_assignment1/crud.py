from sqlalchemy.orm import Session
from . import schema,model
from fastapi import HTTPException
from . import utils
def create_task(db:Session,task : schema.TaskBase):
    try:
        db_task = model.Task(**task.model_dump())
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return db_task
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500,detail=str(e))

def get_all_tasks(db:Session,is_completed:bool | None = None,priority:str | None = None):

    try:
        if is_completed is not None:
            return db.query(model.Task).filter(model.Task.is_completed == is_completed).all()
        elif priority is not None:
            return db.query(model.Task).filter(model.Task.priority == priority).all()
        return db.query(model.Task).all()
    
    except Exception as e:
        raise HTTPException (status_code=500,detail=str(e))
    
def get_task_by_id(db:Session,task_id:int):
    try:
        return db.query(model.Task).filter(model.Task.id == task_id).first()
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))

def delete_task_by_id(db:Session,task_id:int):
    try:
        db.query(model.Task).filter(model.Task.id == task_id).delete()
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))

def update_task(db:Session,task_id:int,task:schema.TaskUpdate):
    try:
        db_task = get_task_by_id(db,task_id)
        update_data = task.dict(exclude_unset=True)

        for key , value in update_data.items():
            setattr(db_task,key,value)

        db.commit()
        db.refresh(db_task)
        return db_task
    
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
    
def create_User(db:Session,user:schema.UserCreate):
    try:
        password = utils.get_password_hash(user.password)
        print(password)
        user.password = password
        db_user = model.User(**user.model_dump())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        print(e)
        db.rollback()
        raise HTTPException(500,detail="could not save user")

def get_user_by_id(db:Session,user_id:int):
    return db.query(model.User).filter(model.User.id == user_id).first()

def add_task_to_user(db:Session,usr_id:int,task:schema.TaskBase):
    try:
        db_user = get_user_by_id(db,usr_id)

        if db_user is None:
            raise HTTPException(404,"user doesn't exist")
        
        db_task = model.Task(**task.model_dump(),user_id=usr_id)
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return db_task
    except Exception as e:
        print(e)
        db.rollback()
        raise HTTPException(500,"could not assign task to user")

    
def get_all_users(db:Session):
    try:
        return db.query(model.User).all()
    except:
        raise HTTPException(500,"could not get users")

def get_user_by_username(db:Session,username:str):  
    try:
        return db.query(model.User).filter(model.User.name == username).first()
    except:
        raise HTTPException(status_code=500,detail="error while finding the user")