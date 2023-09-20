import os
import sys

import pytest

from shared.database import get_db
from shared.db_models import create_notification_channel

# Make sure that the application source directory (this directory's parent) is
# on sys.path.

app_root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, app_root_dir)


@pytest.fixture
def db():
    return list(get_db()).pop()


@pytest.fixture
def notification_channel(db):
    channel_data = {
        "user_id": 5,
        "client_correlator": "123",
        "application_tag": "myTag",
        "channel_type": "WebSockets",
        "channel_data": {
            "channelURL": "ws://localhost/5/channels/ws",
            "maxNotifications": 10,
        },
        "channel_life_time": 3600,
        "callback_url": "http://my_ip/proxy",
    }

    return create_notification_channel(db, **channel_data)
