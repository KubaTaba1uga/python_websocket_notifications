from typing import Optional

from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import PickleType
from sqlalchemy import String
from sqlalchemy.orm import Session

from .database import Base
from .schemas import NotificationChannelUserSchema

# from .spec_utils.channel_data_utils import render_channel_data


class User(Base):
    __tablename__ = "app_user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)


class Message(Base):
    __tablename__ = "message"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, index=True)
    from_ = Column(Integer, ForeignKey("app_user.id"), name="from_", key="from")
    to = Column(Integer, ForeignKey("app_user.id"), name="to_")


class NotificationChannel(Base):
    __tablename__ = "notification_channel"

    id = Column(Integer, primary_key=True, index=True)
    client_correlator = Column(String, nullable=True)
    application_tag = Column(String, nullable=True)
    channel_type = Column(String)
    channel_data = Column(PickleType)
    channel_life_time = Column(Integer)
    user_id = Column(Integer, ForeignKey("app_user.id"))

    # @property
    # def callback_url(self) -> str:
    #     pass


def get_user(db: Session, user_id: int) -> User:
    return db.query(User).filter(User.id == user_id).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> list:
    return db.query(User).offset(skip).limit(limit).all()


def get_notification_channel(
    db: Session, user_id: int, channel_id: int
) -> NotificationChannel:
    return (
        db.query(NotificationChannel)
        .filter(
            NotificationChannel.user_id == user_id, NotificationChannel.id == channel_id
        )
        .first()
    )


def create_notification_channel(
    db: Session, user_id: int, nc: NotificationChannelUserSchema
) -> NotificationChannel:
    db_notification_channel = NotificationChannel(
        user_id=user_id,
        channel_type=nc.channel_type,
        channel_life_time=nc.channel_life_time,
        client_correlator=nc.client_correlator,
        application_tag=nc.application_tag,
    )
    return save_obj(db, db_notification_channel)


def save_obj(db: Session, obj: Base):
    db.add(obj)
    db.commit()
    db.refresh(obj)

    return obj
