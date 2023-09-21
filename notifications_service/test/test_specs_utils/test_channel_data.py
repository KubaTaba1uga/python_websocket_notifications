import re

from notifications_service.src.spec_utils.channel_data_utils import render_channel_data
from notifications_service.src.spec_utils.channel_data_utils import WebsocketChannelData


def test_render_channel_data_max_notifications(notification_channel):
    user_data = {"maxNotifications": 10}
    server_data = render_channel_data(
        notification_channel, user_data, {"domain": "127.0.0.1"}
    )

    assert bool(
        re.search(r"ws://127.0.0.1/5/channels/\d*/ws", server_data["channelURL"])
    )

    for key, value in user_data.items():
        assert value == server_data.get(key)
