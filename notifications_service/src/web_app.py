from fastapi import Depends
from fastapi import FastAPI
from fastapi import Request
from sqlalchemy.orm import Session

from shared.database import get_db

from .app_logic import create_notification_channel as _create_notification_channel
from .app_logic import list_notification_channels as _list_notification_channel
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
)
def create_notification_channel(
    request: Request,
    user_id: int,
    notification_channel: NotificationChannelUserSchema,
    db: Session = Depends(get_db),
):
    # TO-DO validate data
    domain = get_host_domain(request)

    return _create_notification_channel(domain, user_id, notification_channel, db)


def get_host_domain(request: Request) -> str:
    return str(request.base_url.hostname)
