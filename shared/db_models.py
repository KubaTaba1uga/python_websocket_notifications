from typing import List

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import PickleType
from sqlalchemy import String
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from shared.spec_utils.channel_life_time_utils import \
    convert_channel_life_time_to_expiration_date
from shared.spec_utils.channel_life_time_utils import \
    convert_expiration_date_to_channel_life_time

from .database import Base
from .schemas import MessageUserSchema
from .schemas import SubscriptionUserSchema


class User(Base):
    __tablename__ = "app_user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)


class Message(Base):
    __tablename__ = "message"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, index=True)
    from_ = Column(Integer, ForeignKey("app_user.id"), name="from_")
    to = Column(Integer, ForeignKey("app_user.id"), name="to_")


class Duration:
    expiry_date_time = Column(DateTime(timezone=False), server_default=func.now())

    @property
    def duration(self) -> int:
        if None is (duration := getattr(self, "_duration", None)):
            return convert_expiration_date_to_channel_life_time(self.expiry_date_time)
        return duration

    @duration.setter
    def duration(self, duration: int) -> None:
        self.expiry_date_time = convert_channel_life_time_to_expiration_date(duration)

    def overwrite_duration(self, duration: int) -> None:
        # hidden duration attribute is created to allow
        #  ovewriting dynamic creation of it's public equivalent.
        #  this way we can return requested duration,
        #  when in fact few seconds has passed.
        self._duration = duration


class Subscription(Base, Duration):
    __tablename__ = "subscription"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("app_user.id"))
    callback_reference = Column(PickleType)
    filter = Column(String)
    client_correlator = Column(String)
    index = Column(Integer)
    restart_token = Column(String)
    max_events = Column(Integer)
    object_attribute_names = Column(String)
    inline_imdn = Column(Boolean)


def get_user(db: Session, user_id: int) -> User:
    return _get_class_by_id(db, User, user_id)


def list_users(db: Session, skip: int = 0, limit: int = 100) -> list:
    return _list_class(db, User, skip, limit)


def get_message(db: Session, msg_id: int) -> Message:
    return _get_class_by_id(db, Message, msg_id)


def list_messages(db: Session, skip: int = 0, limit: int = 100) -> list:
    return _list_class(db, Message, skip, limit)


def create_messge(db: Session, message: MessageUserSchema) -> Message:
    return Message(from_=message.from_, to=message.to, content=message.content)


def get_subscription(db: Session, user_id: int, subscription_id: int) -> Subscription:
    return _get_class_by_id_and_user_id(db, Subscription, subscription_id, user_id)


def list_subscriptions(
    db: Session, user_id: int, skip: int = 0, limit: int = 100
) -> List[Subscription]:
    return _list_class_by_user_id(db, Subscription, user_id, skip, limit)


def create_subscription(
    db: Session, user_id: int, subscription: SubscriptionUserSchema
) -> Subscription:
    # TO-DO implement restart token logic:
    #  Subscription restart token representing the point after
    #  the change(s) being notified. See section 5.1.4.3.
    #  This value applies to the box as a whole, and can be
    #  used independently of any particular subscription.
    #  Let's take obj creation time as restartToken.
    #  If no restartToken just do not post to /replay.

    return Subscription(
        user_id=user_id,
        callback_reference=subscription.callback_reference,
        filter=subscription.filter,
        client_correlator=subscription.client_correlator,
        index=0,
        restart_token=subscription.restart_token,
        max_events=subscription.max_events,
        duration=subscription.duration,
    )


def delete_subscription(
    db: Session, user_id: int, subscription_id: int
) -> Subscription:
    return _delete_class_by_id_and_user_id(db, Subscription, subscription_id, user_id)


def save_obj(db: Session, obj: Base) -> None:
    db.add(obj)
    db.commit()
    db.refresh(obj)


def _get_class_by_id(db, class_, id_):
    return db.query(class_).filter(class_.id == id_).first()


def _list_class(db, class_, skip, limit):
    return db.query(class_).offset(skip).limit(limit).all()


def _get_class_by_id_and_user_id(db, class_, id_, user_id):
    return db.query(class_).filter(class_.id == id_, class_.user_id == user_id).first()


def _list_class_by_user_id(db, class_, user_id, skip, limit):
    return (
        db.query(class_).filter(class_.user_id == user_id)
        # .offset(skip)
        # .limit(limit)
        .all()
    )


def _delete_class_by_id_and_user_id(db, class_, id_, user_id):
    db.query(class_).filter(class_.user_id == user_id, class_.id == id_).delete()
