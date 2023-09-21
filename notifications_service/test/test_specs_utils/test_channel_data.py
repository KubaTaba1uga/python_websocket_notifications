from shared.spec_utils.channel_data_utils import render_channel_data


def test_render_channel_data_user_lifetime(notification_channel):
    user_data = {"maxNotifications": 10}
    server_data = render_channel_data(notification_channel, user_data)

    for key, value in user_data.items():
        assert value == server_data.get(key)
