# TO-DO fetch from db only when it is necessity, otherwise fetch from API

from copy import copy

import requests

from .utils import create_notification_channel
from .utils import get_notification_channel
from .utils import get_notification_channels_list

APP_URL = "http://127.0.0.1"
NOTIFICATIONS_SERVICE_URL = APP_URL + ":8080"
USER_ID = 5


def test_create_notification_channel():
    test_data = {
        "channelType": "WebSockets",
        "channelLifeTime": 3600,
        "clientCorrelator": "123",
        "applicationTag": "myTag",
        "channelData": {
            "channelURL": "ws://127.0.0.1/{}/channels/{}/ws",
            "maxNotifications": 10,
        },
        "callbackURL": "http://somedummyurl.com/proxy",
        "resourceURL": "http://127.0.0.1/5/channels/1",
        "id": 1,
    }
    expected_data = copy(test_data)
    expected_data["channelData"]["channelURL"] = expected_data["channelData"][
        "channelURL"
    ].format(USER_ID, expected_data["id"])

    response = create_notification_channel(
        NOTIFICATIONS_SERVICE_URL, USER_ID, test_data
    )

    assert response.status_code == 201
    received_data = response.json()

    assert expected_data == received_data


def test_list_notification_channel(notification_channel_fabric):
    expected_responses = [
        notification_channel_fabric({"channelType": "WebSockets"}) for _ in range(10)
    ]

    response = get_notification_channels_list(NOTIFICATIONS_SERVICE_URL, USER_ID)

    assert 200 == response.status_code
    received = response.json()

    assert all(
        any(exp_resp.json()["id"] == rec_c["id"] for rec_c in received)
        for exp_resp in expected_responses
    )


def test_get_notification_channel(notification_channel):
    expected = {
        "channelType": "WebSockets",
        "channelLifeTime": 3599,
        "clientCorrelator": "123",
        "applicationTag": "myTag",
        "channelData": {
            "maxNotifications": 10,
            "channelURL": "ws://127.0.0.1/{}/channels/{}/ws",
        },
        "callbackURL": "http://somedummyurl.com/proxy",
        "resourceURL": "http://127.0.0.1/5/channels/1",
        "id": notification_channel["id"],
    }
    expected["channelData"]["channelURL"] = expected["channelData"][
        "channelURL"
    ].format(USER_ID, expected["id"])

    response = get_notification_channel(
        NOTIFICATIONS_SERVICE_URL, USER_ID, expected["id"]
    )

    assert 200 == response.status_code
    received = response.json()

    assert expected == received


def test_delete_notification_channel(notification_channel):
    URL_FORMAT = NOTIFICATIONS_SERVICE_URL + "/{}/channels/{}"

    response = requests.delete(URL_FORMAT.format(USER_ID, notification_channel["id"]))

    assert 204 == response.status_code

    response = get_notification_channel(
        NOTIFICATIONS_SERVICE_URL, USER_ID, notification_channel["id"]
    )
    assert 404 == response.status_code


def test_get_notification_channels_list_lifetime(notification_channel):
    URL_FORMAT, TIMEOUT = (
        NOTIFICATIONS_SERVICE_URL + "/{}/channels/{}/channelLifetime",
        3,
    )

    expected = {"channelLifeTime": notification_channel["channelLifeTime"]}

    response = requests.get(URL_FORMAT.format(USER_ID, notification_channel["id"]))

    assert 200 == response.status_code

    received = response.json()
    assert received["channelLifeTime"] in range(
        expected["channelLifeTime"] - TIMEOUT, expected["channelLifeTime"]
    )


def test_put_notification_channel_lifetime(notification_channel):
    URL_FORMAT, LIFETIME_IN_SECS = (
        NOTIFICATIONS_SERVICE_URL + "/{}/channels/{}/channelLifetime",
        100,
    )

    expected = {"channelLifeTime": LIFETIME_IN_SECS}

    response = requests.put(
        URL_FORMAT.format(USER_ID, notification_channel["id"]),
        json=expected,
    )

    assert 200 == response.status_code
    assert expected == response.json()
