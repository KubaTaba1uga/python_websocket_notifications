from fastapi import Depends
from fastapi import FastAPI
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


@app.post("/{user_id}/channels")
def create_notification_channel(
    user_id: int,
    notification_channel: NotificationChannelUserSchema,
    db: Session = Depends(get_db),
    response_model=NotificationChannelServerSchema,
):
    # TO-DO validate data
    return _create_notification_channel(user_id, notification_channel, db)
