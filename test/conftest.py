import pytest

from notifications_service.test.conftest import db  # do not remove this line!
from shared.db_models import list_users

from .utils import create_notification_channel

APP_URL = "http://127.0.0.1"
NOTIFICATIONS_SERVICE_URL = APP_URL + ":8080"


@pytest.fixture
def db_users(db):
    return list_users(db)


@pytest.fixture
def notification_channel_fabric(db):
    def local_fabric(test_data, user_id=5):
        return create_notification_channel(
            NOTIFICATIONS_SERVICE_URL, user_id, test_data
        )

    return local_fabric


@pytest.fixture
def notification_channel(notification_channel_fabric):
    response = notification_channel_fabric(
        {
            "clientCorrelator": "123",
            "applicationTag": "myTag",
            "channelType": "WebSockets",
            "channelData": {
                "channelURL": "ws://127.0.0.1/{}/channels/{}/ws",
                "maxNotifications": 10,
            },
            "channelLifeTime": 3600,
        },
        5,
    )
    assert 201 == response.status_code
    return response.json()
