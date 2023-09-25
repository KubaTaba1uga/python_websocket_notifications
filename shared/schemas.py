from typing import Optional

from pydantic import BaseModel
from pydantic import Field

DEFAULT_DURATION = 86400  # 24h in sec
DEFAULT_MAX_EVENTS = 100  # 24h in sec


class DbModel:
    class Config:
        orm_mode = True


class UserSchema(BaseModel, DbModel):
    id: int
    username: str


class MessageUserSchema(BaseModel, DbModel):
    from_: int
    to: int
    content: str


class MessageServerSchema(MessageUserSchema):
    id: int


class SubscriptionUserSchema(BaseModel, DbModel):
    callback_reference: dict
    duration: Optional[int] = Field(default=DEFAULT_DURATION)
    filter: Optional[str] = Field(default="** dummy filter **")
    client_correlator: Optional[str] = Field(default=None)
    restart_token: Optional[str] = Field(default=None)
    max_events: Optional[int] = Field(default=DEFAULT_MAX_EVENTS)
    ## TO-DO implement attributes filtering
    ## TO-DO implement inline imdn boolean
