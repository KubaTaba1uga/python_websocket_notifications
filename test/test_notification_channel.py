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
