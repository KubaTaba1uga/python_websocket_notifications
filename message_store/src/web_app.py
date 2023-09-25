from fastapi import Depends
from fastapi import FastAPI
from fastapi import HTTPException
from sqlalchemy.orm import Session

from shared import db_models
from shared import schemas
from shared.database import get_db

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/users", response_model=list[schemas.UserSchema])
def list_user(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = db_models.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.UserSchema)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db_models.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/messages", response_model=schemas.MessageUserSchema)
def create_message(message: schemas.MessageUserSchema, db: Session = Depends(get_db)):
    pass
