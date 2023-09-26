"""
Let's assume that corresponding data are always valid:
   - user_id
   - message_id
   - subscription_id
Validatin them would unnecessary complicated POC.
"""
from fastapi import Depends
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import Response
from sqlalchemy.orm import Session

from shared import db_models
from shared import schemas
from shared.database import get_db

from .app_logic import create_message as _create_message
from .app_logic import create_subscription as _create_subscription
from .app_logic import delete_subscription as _delete_subscription
from .app_logic import get_messages as _get_message
from .app_logic import get_subscription as _get_subscription
from .app_logic import list_messages as _list_message
from .app_logic import list_subscriptions as _list_subscription
from .app_logic import update_subscription as _update_subscription

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
    sub_db = _create_subscription(user_id, subscription, db)
    sub_db.overwrite_duration(subscription.duration)

    return sub_db


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


@app.post(
    "/{user_id}/subscriptions/{subscription_id}",
    response_model=schemas.SubscriptionServerSchema,
    response_model_by_alias=True,
)
def update_subscription(
    user_id: int,
    subscription_id: int,
    subscription_update: schemas.SubscriptionUpdateSchema,
    db: Session = Depends(get_db),
):
    # Handle special cases
    if 0 == subscription_update.duration:
        subscription_update.duration = schemas.DEFAULT_DURATION

    sub_db = _update_subscription(user_id, subscription_id, subscription_update, db)

    # Mock counter
    if None is not subscription_update.duration:
        sub_db.overwrite_duration(subscription_update.duration)

    return sub_db


@app.delete(
    "/{user_id}/subscriptions/{subscription_id}",
    response_model=schemas.SubscriptionServerSchema,
    response_model_by_alias=True,
)
def delete_subscription(
    user_id: int,
    subscription_id: int,
    db: Session = Depends(get_db),
):
    _delete_subscription(user_id, subscription_id, db)

    return Response(status_code=204)
