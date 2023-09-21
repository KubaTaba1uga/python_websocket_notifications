from typing import List

from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import PickleType
from sqlalchemy import String
from sqlalchemy.orm import Session

from shared.database import Base
from shared.db_models import save_obj

from .schemas import NotificationChannelUserSchema


class NotificationChannel(Base):
    __tablename__ = "notification_channel"

    id = Column(Integer, primary_key=True, index=True)
    client_correlator = Column(String, nullable=True)
    application_tag = Column(String, nullable=True)
    channel_type = Column(String)
    channel_data = Column(PickleType)
    channel_life_time = Column(Integer)
    user_id = Column(Integer, ForeignKey("app_user.id"))


def list_notification_channels(
    db: Session, user_id: int, skip: int = 0, limit: int = 100
) -> List[NotificationChannel]:
    return (
        db.query(NotificationChannel).filter(NotificationChannel.user_id == user_id)
        # .offset(skip)
        # .limit(limit)
        .all()
    )


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


def delete_notification_channel(db: Session, user_id: int, channel_id: int) -> None:
    db.query(NotificationChannel).filter(
        NotificationChannel.user_id == user_id, NotificationChannel.id == channel_id
    ).delete()


def create_notification_channel(
    db: Session, user_id: int, nc: NotificationChannelUserSchema
) -> NotificationChannel:
    db_notification_channel = NotificationChannel(
        user_id=user_id,
        channel_type=nc.channel_type,
        channel_life_time=nc.channel_life_time,
        client_correlator=nc.client_correlator,
        application_tag=nc.application_tag,
        channel_data=nc.channel_data,
    )
    return save_obj(db, db_notification_channel)
