from enum import Enum
from typing import Optional

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field

from shared.schemas import CAMEL_CONFIG

DEFAULT_CHANNEL_LIFE_TIME = 86400  # 24h in sec


# TO-DO improve fields' annotations


class NotificationChannelTypeEnum(str, Enum):
    websockets = "WebSockets"


class NotificationChannelUserSchema(BaseModel):
    model_config = CAMEL_CONFIG

    channel_type: NotificationChannelTypeEnum = Field()
    channel_life_time: int = Field(default=DEFAULT_CHANNEL_LIFE_TIME)
    client_correlator: Optional[str] = Field(default=None)
    application_tag: Optional[str] = Field(default=None)
    channel_data: dict = Field(default={})


class NotificationChannelServerSchema(NotificationChannelUserSchema):
    model_config = CAMEL_CONFIG

    id: int
    resource_U_R_L: str
    callback_U_R_L: str


class NotificationChannelLifeTimeSchema(BaseModel):
    model_config = CAMEL_CONFIG
    channel_life_time: int = Field(default=DEFAULT_CHANNEL_LIFE_TIME)
