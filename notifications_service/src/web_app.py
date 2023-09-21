from fastapi import Depends
from fastapi import FastAPI
from fastapi import Request
from sqlalchemy.orm import Session

from shared.database import get_db
from shared.schemas import NotificationChannelServerSchema
from shared.schemas import NotificationChannelUserSchema

from .crud import create_notification_channel as _create_notification_channel

# from shared.schemas import NotificationChannelCreatedSchema
# from shared.schemas import UserSchema


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


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
