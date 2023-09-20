from sqlalchemy.orm import Session

from shared import db_models
# from shared.database import get_db
# from shared.schemas import NotificationChannelCreatedSchema
from shared.schemas import NotificationChannelUserSchema

# from shared.schemas import UserSchema

# from .config import get_proxy_endpoint_url


def create_notification_channel(
    user_id: int, notification_channel: NotificationChannelUserSchema, db: Session
) -> NotificationChannelUserSchema:
    new_nc = db_models.create_notification_channel(
        db,
        user_id,
        notification_channel.channelType,
        notification_channel.channelLifeTime,
        notification_channel.clientCorrelator,
        notification_channel.applicationTag,
    )

    return new_nc
