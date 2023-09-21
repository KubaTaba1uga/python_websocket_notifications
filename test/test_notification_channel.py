from copy import copy

import requests
from fastapi.testclient import TestClient

APP_URL = "http://127.0.0.1"
NOTIFICATIONS_SERVICE_URL = APP_URL + ":8080"


def test_create_notification_channel():
    URL_FORMAT = NOTIFICATIONS_SERVICE_URL + "/{}/channels"

    test_data = {
        "clientCorrelator": "123",
        "applicationTag": "myTag",
        "channelType": "WebSockets",
        "channelData": {
            "channelURL": "ws://localhost/5/channels/ws",
            "maxNotifications": 10,
        },
        "channelLifeTime": 3600,
    }

    expected_data = copy(test_data) | {"id": 1, "user_id": 5}

    response = requests.post(
        URL_FORMAT.format(expected_data["user_id"]), json=test_data
    )

    assert response.status_code == 200
    received_data = response.json()

    assert expected_data == received_data
