from enum import Enum
from typing import Optional

from pydantic import BaseModel
from pydantic import Field

DEFAULT_CHANNEL_LIFE_TIME = 86400  # 24h in sec


class DbModel:
    class Config:
        orm_mode = True


class NotificationChannelTypeEnum(str, Enum):
    websockets = "WebSockets"


class NotificationChannelUserSchema(BaseModel, DbModel):
    channel_type: NotificationChannelTypeEnum = Field(validation_alias="channelType")
    channel_life_time: Optional[int] = Field(
        validation_alias="channelLifeTime", default=DEFAULT_CHANNEL_LIFE_TIME
    )
    client_correlator: Optional[str] = Field(
        validation_alias="clientCorrelator", default=None
    )
    application_tag: Optional[str] = Field(
        validation_alias="applicationTag", default=None
    )
    channel_data: Optional[dict] = Field(validation_alias="channelData", default={})


class NotificationChannelServerSchema(NotificationChannelUserSchema):
    callbackURL: str
    resourceURL: str
    user_id: int
    id: int


class UserSchema(BaseModel, DbModel):
    id: int
    username: str


class MessageSchema(BaseModel, DbModel):
    id: int
    from_: int
    to: int
    content: str
