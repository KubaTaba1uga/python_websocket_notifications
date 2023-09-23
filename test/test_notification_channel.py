# TO-DO fetch from db only when it is necessity, otherwise fetch from API

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

    assert response.status_code == 201
    received_data = response.json()

    expected_data["id"] = received_data["id"]
    expected_data["channelData"]["channelURL"] = expected_data["channelData"][
        "channelURL"
    ].format(USER_ID, expected_data["id"])

    assert expected_data == received_data


def test_list_notification_channel(notification_channel_fabric):
    URL_FORMAT = NOTIFICATIONS_SERVICE_URL + "/{}/channels"

    expected_channels = [notification_channel_fabric() for _ in range(10)]

    user_id = expected_channels[0].user_id

    response = requests.get(URL_FORMAT.format(user_id))

    assert 200 == response.status_code
    received = response.json()

    assert all(
        any(exp_c.id == rec_c["id"] for rec_c in received)
        for exp_c in expected_channels
    )


def test_get_notification_channel(notification_channel):
    URL_FORMAT = NOTIFICATIONS_SERVICE_URL + "/{}/channels/{}"

    expected = {
        "channelType": "WebSockets",
        "channelLifeTime": 3599,
        "clientCorrelator": "123",
        "applicationTag": "myTag",
        "channelData": {"maxNotifications": 10},
        "id": 1,
    }

    response = requests.get(
        URL_FORMAT.format(notification_channel.user_id, notification_channel.id)
    )

    assert 200 == response.status_code
    received = response.json()

    assert received == expected


def test_delete_notification_channel(notification_channel):
    URL_FORMAT = NOTIFICATIONS_SERVICE_URL + "/{}/channels/{}"

    response = requests.delete(
        URL_FORMAT.format(notification_channel.user_id, notification_channel.id)
    )

    assert 204 == response.status_code


def test_get_notification_channel_lifetime(notification_channel):
    URL_FORMAT = NOTIFICATIONS_SERVICE_URL + "/{}/channels/{}/channelLifetime"

    expected = {"channelLifeTime": notification_channel.channel_life_time}

    print(expected)
    print(notification_channel.expiry_date_time)

    response = requests.get(
        URL_FORMAT.format(notification_channel.user_id, notification_channel.id)
    )

    assert 200 == response.status_code
    assert expected == response.json()


def test_put_notification_channel_lifetime(notification_channel):
    URL_FORMAT, LIFETIME_IN_SECS = (
        NOTIFICATIONS_SERVICE_URL + "/{}/channels/{}/channelLifetime",
        100,
    )

    expected = {"channelLifeTime": LIFETIME_IN_SECS}

    response = requests.put(
        URL_FORMAT.format(notification_channel.user_id, notification_channel.id),
        json=expected,
    )

    assert 200 == response.status_code
    assert expected == response.json()
