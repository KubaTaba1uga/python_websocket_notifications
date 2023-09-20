from copy import copy

from shared.db_models import create_notification_channel
from shared.db_models import NotificationChannel


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
        "callback_url": "http://my_ip/proxy",
    }

    expected_data = copy(test_data) | {"id": 1}
    expected_data["user"] = expected_data.pop("user_id")

    create_notification_channel(db, **test_data)

    received = (
        db.query(NotificationChannel)
        .filter(NotificationChannel.id == expected_data["id"])
        .first()
    )

    for expected_key, expected_value in expected_data.items():
        assert expected_value == getattr(received, expected_key)
