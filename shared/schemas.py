from typing import Optional

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field
from pydantic import model_validator

DEFAULT_DURATION = 86400  # 24h in sec
DEFAULT_MAX_EVENTS = 100


def to_camel(string: str) -> str:
    string_parts = string.split("_")
    lowercase = string_parts.pop(0)
    return lowercase + "".join(word.capitalize() for word in string_parts)


CAMEL_CONFIG = ConfigDict(
    orm_mode=True,
    alias_generator=to_camel,
    populate_by_name=True,
)


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


class SubscriptionUpdateSchema(BaseModel, DbModel):
    model_config = CAMEL_CONFIG

    duration: Optional[int] = None
    restart_token: Optional[str] = None

    @model_validator(mode="before")
    def check_duration_or_restart_token(cls, values):
        if (values.get("duration") is None) and (values.get("restartToken") is None):
            raise ValueError("either duration or restartToken is required")

        return values


class SubscriptionUserSchema(SubscriptionUpdateSchema):
    callback_reference: dict
    duration: int = Field(default=DEFAULT_DURATION)
    # TO-DO by default match all events
    filter: Optional[str] = Field(default="** dummy filter **")
    client_correlator: Optional[str] = Field(default=None)
    max_events: Optional[int] = Field(default=DEFAULT_MAX_EVENTS)
    ## TO-DO implement attributes filtering
    ## TO-DO implement inline imdn boolean

    @model_validator(mode="after")
    def check_duration_or_restart_token(cls, values):
        return values


class SubscriptionServerSchema(SubscriptionUserSchema):
    id: int
    index: int
