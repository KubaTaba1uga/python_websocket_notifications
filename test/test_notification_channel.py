from copy import copy

import requests
from fastapi.testclient import TestClient

APP_URL = "http://127.0.0.1"
NOTIFICATIONS_SERVICE_URL = APP_URL + ":8080"


def test_create_notification_channel():
    URL_FORMAT, USER_ID = NOTIFICATIONS_SERVICE_URL + "/{}/channels", 5

    test_data = {
        "clientCorrelator": "123",
        "applicationTag": "myTag",
        "channelType": "WebSockets",
        "channelData": {
            "channelURL": "ws://127.0.0.1/{}/channels/{}/ws",
            "maxNotifications": 10,
        },
        "channelLifeTime": 3600,
    }

    expected_data = copy(test_data)

    response = requests.post(URL_FORMAT.format(USER_ID), json=test_data)

    assert response.status_code == 200
    received_data = response.json()

    expected_data["id"] = received_data["id"]
    expected_data["channelData"]["channelURL"] = expected_data["channelData"][
        "channelURL"
    ].format(USER_ID, expected_data["id"])

    assert expected_data == received_data


def test_list_notification_channel(notification_channel_fabric):
    URL_FORMAT, USER_ID = NOTIFICATIONS_SERVICE_URL + "/{}/channels", 5

    expected_channels = [notification_channel_fabric() for _ in range(10)]

    response = requests.get(URL_FORMAT.format(USER_ID))

    assert 200 == response.status_code
    received = response.json()

    assert all(
        any(exp_c.id == rec_c["id"] for rec_c in received)
        for exp_c in expected_channels
    )


def test_get_notification_channel(notification_channel):
    URL_FORMAT, USER_ID = (
        NOTIFICATIONS_SERVICE_URL + "/{}/channels/{}",
        5,
    )

    expected = {
        "channelType": "WebSockets",
        "channelLifeTime": 3600,
        "clientCorrelator": "123",
        "applicationTag": "myTag",
        "channelData": {"maxNotifications": 10},
        "id": 1,
    }

    response = requests.get(URL_FORMAT.format(USER_ID, notification_channel.id))

    assert 200 == response.status_code
    received = response.json()

    assert received == expected
