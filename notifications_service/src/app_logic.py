from typing import List

from sqlalchemy.orm import Session

from . import db_models
from .schemas import NotificationChannelLifeTimeSchema
from .schemas import NotificationChannelUserSchema
from .spec_utils.channel_data_utils import render_channel_data


def create_notification_channel(
    domain: str,
    user_id: int,
    notification_channel: NotificationChannelUserSchema,
    db: Session,
) -> db_models.NotificationChannel:
    new_nc = db_models.create_notification_channel(db, user_id, notification_channel)
    db_models.save_obj(db, new_nc)

    new_nc.channel_data = render_channel_data(
        new_nc, notification_channel.channel_data, {"domain": domain}
    )
    db_models.save_obj(db, new_nc)

    return new_nc


def list_notification_channels(
    user_id: int,
    db: Session,
) -> List[db_models.NotificationChannel]:
    return db_models.list_notification_channels(db, user_id)


def get_notification_channel(
    user_id: int, nc_id: int, db: Session
) -> db_models.NotificationChannel:
    return db_models.get_notification_channel(db, user_id, nc_id)


def delete_notification_channel(user_id: int, nc_id: int, db: Session) -> None:
    db_models.delete_notification_channel(db, user_id, nc_id)
    db.commit()
    return None


def update_notification_channel_life_time(
    user_id: int, nc_id: int, lifetime: NotificationChannelLifeTimeSchema, db: Session
) -> None:
    new_nc = db_models.get_notification_channel(db, user_id, nc_id)
    new_nc.channel_life_time = lifetime.channel_life_time
    db_models.save_obj(db, new_nc)
    return None
