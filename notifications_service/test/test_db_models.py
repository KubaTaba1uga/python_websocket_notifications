from copy import copy

from notifications_service.src.db_models import create_notification_channel
from notifications_service.src.db_models import get_notification_channel
from notifications_service.src.db_models import list_notification_channels
from notifications_service.src.db_models import NotificationChannel
from notifications_service.src.schemas import NotificationChannelUserSchema


def test_create_notification_channel_success(db):
    test_data = {
        "user_id": 5,
        "client_correlator": "123",
        "application_tag": "myTag",
        "channel_type": "WebSockets",
        "channel_life_time": 3600,
        "channel_data": {"maxNotifications": 10},
    }

    expected_data = copy(test_data)

    nc = NotificationChannelUserSchema(
        channelType=test_data["channel_type"],
        channelLifeTime=test_data["channel_life_time"],
        clientCorrelator=test_data["client_correlator"],
        applicationTag=test_data["application_tag"],
        channelData=test_data["channel_data"],
    )

    received = create_notification_channel(db, test_data["user_id"], nc)

    for expected_key, expected_value in expected_data.items():
        assert expected_value == getattr(received, expected_key)


def test_get_notification_channel(db, notification_channel):
    received = get_notification_channel(
        db, notification_channel.user_id, notification_channel.id
    )

    assert notification_channel == received


# TO-DO change limit for some resonable value, best add
#  offset for current ammount off channels.
def test_list_notification_channel(db, notification_channel_fabric):
    channels_list = [notification_channel_fabric() for _ in range(10)]

    nc = channels_list[0]

    received = list_notification_channels(db, nc.user_id, limit=1000000)

    assert all(
        any(exp_c.id == rec_c.id for rec_c in received) for exp_c in channels_list
    )
