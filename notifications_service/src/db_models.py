from datetime import datetime
from typing import List
from typing import Optional

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import PickleType
from sqlalchemy import String
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from shared.database import Base
from shared.db_models import save_obj

from .config import get_proxy_endpoint_url
from .schemas import NotificationChannelUserSchema
from .spec_utils.channel_life_time_utils import \
    convert_channel_life_time_to_expiration_date
from .spec_utils.channel_life_time_utils import \
    convert_expiration_date_to_channel_life_time


class ChannelLifeTime:
    expiry_date_time = Column(DateTime(timezone=False), server_default=func.now())

    @property
    def channel_life_time(self) -> int:
        if None is (life_time := getattr(self, "_life_time", None)):
            return convert_expiration_date_to_channel_life_time(self.expiry_date_time)
        return life_time

    @channel_life_time.setter
    def channel_life_time(self, life_time: int) -> None:
        self.expiry_date_time = convert_channel_life_time_to_expiration_date(life_time)

    def overwrite_channel_life_time(self, life_time: int) -> None:
        # hidden life time attribute is created to allow
        #  ovewriting dynamic creation of it's public equivalent.
        #  this way we can return requested life time,
        #  when in fact few seconds has passed.
        self._life_time = life_time


class ResourceURL:
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("app_user.id"))

    def format_resource_url(self) -> str:
        return f"/{self.user_id}/channels/{self.id}"

    @property
    def resource_U_R_L(self) -> str:
        return getattr(self, "_resource_url_prefix", "") + self.format_resource_url()

    def set_resource_url_prefix(self, prefix: str) -> None:
        self._resource_url_prefix = prefix


class CallbackURL:
    @property
    def callback_U_R_L(self) -> str:
        return get_proxy_endpoint_url()


class NotificationChannel(Base, ChannelLifeTime, ResourceURL, CallbackURL):
    __tablename__ = "notification_channel"
    
    id = Column(Integer, primary_key=True, index=True)
    client_correlator = Column(String, nullable=True)
    application_tag = Column(String, nullable=True)
    channel_type = Column(String)
    channel_data = Column(PickleType)
    expiry_date_time = Column(DateTime(timezone=False), server_default=func.now())
    user_id = Column(Integer, ForeignKey("app_user.id"))
    
    @property
    def resource_U_R_L(self) -> str:
        return "dummy.url.com"
        
    @property
    def channel_life_time(self) -> int:
        return 0

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
    db: Session,
    user_id: int,
    nc: NotificationChannelUserSchema,
) -> NotificationChannel:
    db_notification_channel = NotificationChannel(
        user_id=user_id,
        channel_type=nc.channel_type,
        client_correlator=nc.client_correlator,
        application_tag=nc.application_tag,
        channel_data=nc.channel_data,
        expiry_date_time=convert_channel_life_time_to_expiration_date(
            nc.channel_life_time
        ),
    )

    return save_obj(db, db_notification_channel)
