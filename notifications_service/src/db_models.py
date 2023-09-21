from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import PickleType
from sqlalchemy import String
from sqlalchemy.orm import Session

from shared.db_models import save_obj

from .database import Base
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
