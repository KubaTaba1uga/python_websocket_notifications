from copy import copy

from shared.db_models import create_notification_channel
from shared.db_models import get_notification_channel
from shared.db_models import NotificationChannel
from shared.schemas import NotificationChannelUserSchema


def test_create_notification_channel_success(db):
    test_data = {
        "user_id": 5,
        "client_correlator": "123",
        "application_tag": "myTag",
        "channel_type": "WebSockets",
        "channel_data": {
            "channelURL": "ws://localhost/5/channels/ws",
            "maxNotifications": 10,
        },
        "channel_life_time": 3600,
    }

    expected_data = copy(test_data) | {"id": 1}

    nc = NotificationChannelUserSchema(
        channelType=test_data["channel_type"],
        channelLifeTime=test_data["channel_life_time"],
        clientCorrelator=test_data["client_correlator"],
        applicationTag=test_data["application_tag"],
        channelData=test_data["channel_data"],
    )

    create_notification_channel(db, test_data["user_id"], nc)

    received = (
        db.query(NotificationChannel)
        .filter(NotificationChannel.id == expected_data["id"])
        .first()
    )

    for expected_key, expected_value in expected_data.items():
        assert expected_value == getattr(received, expected_key)


def test_get_notification_channel(db, notification_channel):
    received = get_notification_channel(
        db, notification_channel.user_id, notification_channel.id
    )

    assert notification_channel == received
