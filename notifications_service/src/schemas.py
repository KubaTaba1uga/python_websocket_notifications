from typing import Optional

from pydantic import BaseModel
from pydantic import Field


class DbModel:
    class Config:
        orm_mode = True


class NotificationChannelBaseSchema(BaseModel, DbModel):
    id: int
    user_id: int
    channelType: str = Field(alias="channel_type")
    channelLifeTime: Optional[int] = Field(alias="channel_life_time")
    clientCorrelator: Optional[str] = Field(alias="client_correlator")
    applicationTag: Optional[str] = Field(alias="application_tag")


class NotificationChannelCreatedSchema(NotificationChannelBaseSchema):
    channelData: dict = Field(alias="channel_data")
    callbackURL: str = Field(alias="callback_url")
    resourceURL: str
