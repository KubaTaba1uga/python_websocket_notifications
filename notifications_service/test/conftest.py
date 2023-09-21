import os
import sys

import pytest

from shared.database import get_db
from shared.db_models import create_notification_channel
from shared.schemas import NotificationChannelUserSchema

# Make sure that the application source directory (this directory's parent) is
# on sys.path.

app_root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, app_root_dir)


@pytest.fixture
def db():
    return list(get_db()).pop()


@pytest.fixture
def notification_channel(db):
    nc = NotificationChannelUserSchema(
        channelType="WebSockets",
        channelLifeTime=3600,
        clientCorrelator="123",
        applicationTag="myTag",
        channelData={
            "channelURL": "ws://localhost/5/channels/ws",
            "maxNotifications": 10,
        },
    )

    return create_notification_channel(db, 5, nc)
