from typing import List

from sqlalchemy.orm import Session

from shared import db_models
from shared import schemas


def create_message(
    msg_schema: schemas.MessageUserSchema, db: Session
) -> db_models.Message:
    msg_db = db_models.create_messge(db, msg_schema)
    db_models.save_obj(db, msg_db)

    return msg_db


def list_messages(db: Session) -> List[db_models.Message]:
    return db_models.list_messages(db)


def get_messages(msg_id: int, db: Session) -> List[db_models.Message]:
    return db_models.get_message(db, msg_id)


def create_subscription(
    user_id: int, subscription_schema: schemas.SubscriptionUserSchema, db: Session
) -> db_models.Subscription:
    subscription_db = db_models.create_subscription(db, user_id, subscription_schema)
    db_models.save_obj(db, subscription_db)

    return subscription_db


def list_subscriptions(user_id: int, db: Session) -> List[db_models.Subscription]:
    return db_models.list_subscriptions(db, user_id=user_id)


def get_subscription(
    user_id: int, subscription_id: int, db: Session
) -> List[db_models.Subscription]:
    return db_models.get_subscription(db, user_id, subscription_id)
