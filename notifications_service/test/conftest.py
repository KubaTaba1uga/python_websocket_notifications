import os
import sys

import pytest

from notifications_service.src.db_models import create_notification_channel
from notifications_service.src.schemas import NotificationChannelUserSchema
from shared.database import get_db

# Make sure that the application source directory (this directory's parent) is
# on sys.path.

app_root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, app_root_dir)


@pytest.fixture
def db():
    return list(get_db()).pop()


@pytest.fixture
def notification_channel_fabric(db):
    def _(
        user_id=5,
        type="WebSockets",
        life_time=3600,
        cc="123",
        at="myTag",
        cd={
            "maxNotifications": 10,
        },
    ):
        nc = NotificationChannelUserSchema(
            channelType=type,
            channelLifeTime=life_time,
            clientCorrelator=cc,
            applicationTag=at,
            channelData=cd,
        )

        return create_notification_channel(db, user_id, nc)

    return _


@pytest.fixture
def notification_channel(notification_channel_fabric):
    return notification_channel_fabric(
        5,
        "WebSockets",
        3600,
        "123",
        "myTag",
        {
            "maxNotifications": 10,
        },
    )
