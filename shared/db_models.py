from typing import Optional

from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import PickleType
from sqlalchemy import String
from sqlalchemy.orm import Session

from .database import Base

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
    callback_url = Column(String)
    user_id = Column(Integer, ForeignKey("app_user.id"))


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
            NotificationChannel.user == user_id, NotificationChannel.id == channel_id
        )
        .first()
    )


# TO-DO do not save callback_url, it can be generated by the app
# TO-DO pass schema obj instead of many args/kwargs
def create_notification_channel(
    db: Session,
    user_id: int,
    channel_type: str,
    channel_life_time: Optional[int] = None,
    client_correlator: Optional[str] = None,
    application_tag: Optional[str] = None,
) -> NotificationChannel:
    db_notification_channel = NotificationChannel(
        user_id=user_id,
        channel_type=channel_type,
        channel_life_time=channel_life_time,
        client_correlator=client_correlator,
        application_tag=application_tag,
    )
    db.add(db_notification_channel)
    db.commit()
    db.refresh(db_notification_channel)

    return db_notification_channel
