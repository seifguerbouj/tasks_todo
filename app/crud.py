from sqlalchemy.orm import Session
from .models import Task as DBTask
from .schema import Task as PydanticTask
from .schema import User as PydanticUser
from .models import User as DBUser



# def create_task(db: Session, title:str,descripuser:DBUser):
#     if user:
#         username = user.username
#         db_task = DBTask(**task.dict(), owner_name=username)
#         db.add(db_task)
#         db.commit()
#         db.refresh(db_task)
#         return PydanticTask.from_orm(db_task)
#     return "Could not find user"
#     db_task = DBTask(**task.dict())
#     db.add(db_task)
#     db.commit()
#     db.refresh(db_task)
#     return PydanticTask.from_orm(db_task)

def get_tasks(db: Session,username):
    tasks = db.query(DBTask).filter(DBTask.owner_name == username).all()
    return [PydanticTask.from_orm(task) for task in tasks]

def get_task(db: Session, task_id: int):
    task = db.query(DBTask).filter(DBTask.id == task_id).first()
    if task:
        return PydanticTask.from_orm(task)
    return None

def update_task(db: Session, task_id: int, title: str, description: str ,completed:str):
    task = db.query(DBTask).filter(DBTask.id == task_id).first()
    if task:
        task.title = title
        task.description = description
        task.completed=completed
        db.commit()
        return PydanticTask.from_orm(task)
    return None

def delete_task(db: Session, task_id: int):
    task = db.query(DBTask).filter(DBTask.id == task_id).first()
    if task:
        db.delete(task)
        db.commit()
        return PydanticTask.from_orm(task)
    return None

def delete_all_tasks(db: Session):
    tasks = db.query(DBTask).all()
    db.query(DBTask).delete()
    db.commit()
    return [PydanticTask.from_orm(task) for task in tasks]
