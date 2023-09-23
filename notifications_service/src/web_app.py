"""
Let's assume that corresponding data are always valid:
   - user_id
   - notification_channel_id
Unnecessary complications for POC.
"""
from functools import wraps

from fastapi import Depends
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import Request
from fastapi import Response
from sqlalchemy.orm import Session

from shared.database import get_db

from .app_logic import create_notification_channel as _create_notification_channel
from .app_logic import delete_notification_channel as _delete_notification_channel
from .app_logic import get_notification_channel as _get_notification_channel
from .app_logic import list_notification_channels as _list_notification_channel
from .app_logic import \
    update_notification_channel_life_time as _update_notification_channel_life_time
from .schemas import NotificationChannelLifeTimeSchema
from .schemas import NotificationChannelServerSchema
from .schemas import NotificationChannelUserSchema

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get(
    "/{user_id}/channels",
    response_model=list[NotificationChannelServerSchema],
    response_model_by_alias=True,
)
def list_notification_channel(
    user_id: int,
    db: Session = Depends(get_db),
):
    return _list_notification_channel(user_id, db)


@app.post(
    "/{user_id}/channels",
    response_model=NotificationChannelServerSchema,
    response_model_by_alias=True,
    status_code=201,
)
def create_notification_channel(
    request: Request,
    user_id: int,
    notification_channel: NotificationChannelUserSchema,
    db: Session = Depends(get_db),
):
    # TO-DO indexing should be counted per user, not per whole table
    domain = get_host_domain(request)

    nc_db = _create_notification_channel(domain, user_id, notification_channel, db)
    # Thanks to overwriting, response and request have matching life time
    # In real counter started when db object has been created.
    nc_db.overwrite_channel_life_time(notification_channel.channel_life_time)

    return nc_db


@app.get(
    "/{user_id}/channels/{notification_channel_id}",
    response_model=NotificationChannelServerSchema,
    response_model_by_alias=True,
)
def get_notification_channel(
    request: Request,
    user_id: int,
    notification_channel_id: int,
    db: Session = Depends(get_db),
):
    domain = get_host_domain(request)
    nc = _get_notification_channel(domain, user_id, notification_channel_id, db)
    if None is nc:  # this is implemented so integration tests are easier, all data passed
       # to application logic, need to be validated first
        raise HTTPException(status_code=404)

    return nc


@app.delete(
    "/{user_id}/channels/{notification_channel_id}",
)
def delete_notification_channel(
    user_id: int,
    notification_channel_id: int,
    db: Session = Depends(get_db),
):
    _delete_notification_channel(user_id, notification_channel_id, db)

    return Response(status_code=204)


@app.get(
    "/{user_id}/channels/{notification_channel_id}/channelLifetime",
    response_model=NotificationChannelLifeTimeSchema,
    response_model_by_alias=True,
)
def get_notification_channel_lifetime(
    request: Request,
    user_id: int,
    notification_channel_id: int,
    db: Session = Depends(get_db),
):
    domain = get_host_domain(request)
    nc = _get_notification_channel(domain, user_id, notification_channel_id, db)

    return NotificationChannelLifeTimeSchema(channel_life_time=nc.channel_life_time)


@app.put(
    "/{user_id}/channels/{notification_channel_id}/channelLifetime",
    response_model=NotificationChannelLifeTimeSchema,
    response_model_by_alias=True,
)
def update_notification_channel_lifetime(
    user_id: int,
    notification_channel_id: int,
    notification_channel_life_time: NotificationChannelLifeTimeSchema,
    db: Session = Depends(get_db),
):
    _update_notification_channel_life_time(
        user_id, notification_channel_id, notification_channel_life_time, db
    )

    return notification_channel_life_time


def get_host_domain(request: Request) -> str:
    return str(request.base_url.hostname)
