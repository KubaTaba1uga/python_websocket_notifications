from typing import Optional

from pydantic import BaseModel
from pydantic import Field


class DbModel:
    class Config:
        orm_mode = True


class NotificationChannelUserSchema(BaseModel, DbModel):
    channelType: str = Field(serialization_alias="channel_type")
    channelLifeTime: Optional[int] = Field(
        serialization_alias="channel_life_time", default=None
    )
    clientCorrelator: Optional[str] = Field(
        serialization_alias="client_correlator", default=None
    )
    applicationTag: Optional[str] = Field(
        serialization_alias="application_tag", default=None
    )
    channelData: Optional[dict] = Field(
        serialization_alias="channel_data", default=None
    )


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
