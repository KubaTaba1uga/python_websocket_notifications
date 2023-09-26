from fastapi import Depends
from fastapi import FastAPI
from fastapi import HTTPException
from sqlalchemy.orm import Session

from shared import db_models
from shared import schemas
from shared.database import get_db

from .app_logic import create_message as _create_message
from .app_logic import create_subscription as _create_subscription
from .app_logic import get_messages as _get_message
from .app_logic import get_subscription as _get_subscription
from .app_logic import list_messages as _list_message
from .app_logic import list_subscriptions as _list_subscription

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/users", response_model=list[schemas.UserSchema])
def list_user(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = db_models.list_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.UserSchema)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db_models.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post(
    "/messages",
    response_model=schemas.MessageServerSchema,
    response_model_by_alias=True,
)
def create_message(message: schemas.MessageUserSchema, db: Session = Depends(get_db)):
    return _create_message(message, db)


@app.get(
    "/messages",
    response_model=list[schemas.MessageServerSchema],
    response_model_by_alias=True,
)
def list_message(db: Session = Depends(get_db)):
    return _list_message(db)


@app.get(
    "/messages/{msg_id}",
    response_model=schemas.MessageServerSchema,
    response_model_by_alias=True,
)
def get_message(msg_id: int, db: Session = Depends(get_db)):
    return _get_message(msg_id, db)


@app.post(
    "/{user_id}/subscriptions",
    response_model=schemas.SubscriptionServerSchema,
    response_model_by_alias=True,
    status_code=201,
)
def create_subscription(
    user_id: int,
    subscription: schemas.SubscriptionUserSchema,
    db: Session = Depends(get_db),
):
    return _create_subscription(user_id, subscription, db)


@app.get(
    "/{user_id}/subscriptions",
    response_model=list[schemas.SubscriptionServerSchema],
    response_model_by_alias=True,
    status_code=200,
)
def list_subscription(
    user_id: int,
    db: Session = Depends(get_db),
):
    return _list_subscription(user_id, db)


@app.get(
    "/{user_id}/subscriptions/{subscription_id}",
    response_model=schemas.SubscriptionServerSchema,
    response_model_by_alias=True,
)
def get_subscription(
    user_id: int,
    subscription_id: int,
    db: Session = Depends(get_db),
):
    return _get_subscription(user_id, subscription_id, db)
