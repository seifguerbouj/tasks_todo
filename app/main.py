from fastapi import Depends, FastAPI, HTTPException, status, Request, Form
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from jose import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
import secrets
try:

    from database import SessionLocal,create_tables
    from models import User,Task
    #from schema import Task
    from crud import  get_task, get_tasks, update_task, delete_task, delete_all_tasks
except:
    from .database import SessionLocal,create_tables
    from .models import User,Task
    #from .schema import Task
    from .crud import get_task, get_tasks, update_task, delete_task, delete_all_tasks
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

app = FastAPI(docs_url="/docs", redoc_url="/redoc")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


SECRET_KEY = secrets.token_urlsafe(32)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Function to generate an access token
def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Dependency function to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

create_tables()
# Dependency function to authenticate user
async def authenticate_user(username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user or not pwd_context.verify(password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    return user

# Route to generate access token
@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = await authenticate_user(form_data.username, form_data.password, db=db)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

# Route to sign up
@app.post("/signup/")
async def signup(username: str, password: str, db: Session = Depends(get_db)):
    hashed_password = pwd_context.hash(password)
    user = User(username=username, password=hashed_password)
    db.add(user)
    db.commit()
    return {"message": "User created successfully"}

# Protected routes requiring authentication
@app.post("/tasks/")
async def create_task_api(title:str,description:str,completed:bool, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        # Decode the JWT token to extract user information
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        # Fetch user from the database using the username
        user = db.query(User).filter(User.username == username).first()
        # Create task associated with the user
        if user:
            task=Task(title=title,description=description,completed=completed,owner_name=username)
            db.add(task)
            db.commit()
            db.refresh(task)
            return task 
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    except jwt.JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")

@app.get("/tasks/")
async def read_tasks( token: User = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username = payload.get("sub")
    return get_tasks(db=db,username=username )

@app.get("/done/")
async def get_tasks_completed(db: Session = Depends(get_db),token: User = Depends(oauth2_scheme)):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username = payload.get("sub")
        # Fetch user from the database using the username
    user = db.query(User).filter(User.username == username).first()
        # Create task associated with the user
    if user:
        tasks = db.query(Task).filter(Task.completed == True).all()
        return tasks
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


@app.get("/tasks/{task_id}")
async def read_task(task_id: int, token: User = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username = payload.get("sub")
        # Fetch user from the database using the username
    user = db.query(User).filter(User.username == username).first()
        # Create task associated with the user
    if user:
        return get_task(db=db, task_id=task_id)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

@app.put("/tasks/{task_id}")
async def update_task_api(task_id: int, title: str, completed:bool,description: str, token: User = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username = payload.get("sub")
        # Fetch user from the database using the username
    user = db.query(User).filter(User.username == username).first()
        # Create task associated with the user
    if user:
        return update_task(db=db, task_id=task_id, title=title, description=description,completed=completed)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


@app.delete("/tasks/{task_id}")
async def delete_task_api(task_id: int, token: User = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username = payload.get("sub")
        # Fetch user from the database using the username
    user = db.query(User).filter(User.username == username).first()
        # Create task associated with the user
    if user:
        return delete_task(db=db, task_id=task_id)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

@app.delete("/tasks/")
async def delete_all_tasks_api(token: User = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username = payload.get("sub")
        # Fetch user from the database using the username
    user = db.query(User).filter(User.username == username).first()
        # Create task associated with the user
    if user:
        return delete_all_tasks(db=db)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
