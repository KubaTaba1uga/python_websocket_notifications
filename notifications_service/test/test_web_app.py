from copy import copy

import pytest
from fastapi.testclient import TestClient

from notifications_service.src.db_models import get_notification_channel
from notifications_service.src.web_app import app

client = TestClient(app)


# def test_list_notification_channels_no_channels():
#     USER_ID = 1
#     response = client.get(f"/{USER_ID}/channels")
#     assert 200 == response.status_code
#     assert [] == response.json()


def test_list_notification_channels_success(notification_channel):
    USER_ID = 1
    response = client.get(f"/{USER_ID}/channels")
    assert 200 == response.status_code
    assert [] == response.json()


@pytest.mark.parametrize(
    "test_data, expected_data",
    [
        pytest.param(
            {
                "channelType": "WebSockets",
            },
            {
                "channelType": "WebSockets",
                "channelLifeTime": 86400,
                "clientCorrelator": None,
                "applicationTag": None,
                "channelData": {
                    "channelURL": "ws://testserver/5/channels/1/ws",
                    "maxNotifications": 7200,
                },
                "id": 1,
            },
            id="type",
        ),
        pytest.param(
            {
                "channelType": "WebSockets",
                "channelLifeTime": 100,
            },
            {
                "channelType": "WebSockets",
                "channelLifeTime": 100,
                "clientCorrelator": None,
                "applicationTag": None,
                "channelData": {
                    "channelURL": "ws://testserver/5/channels/2/ws",
                    "maxNotifications": 7200,
                },
                "id": 2,
            },
            id="type + lifetime",
        ),
        pytest.param(
            {
                "channelType": "WebSockets",
                "channelLifeTime": 100,
                "channelData": {
                    "channelURL": "this will be overwitten so whatever",
                    "maxNotifications": 100,
                },
            },
            {
                "channelType": "WebSockets",
                "channelLifeTime": 100,
                "clientCorrelator": None,
                "applicationTag": None,
                "channelData": {
                    "channelURL": "ws://testserver/5/channels/3/ws",
                    "maxNotifications": 100,
                },
                "id": 3,
            },
            id="type + lifetime + channel data",
        ),
        pytest.param(
            {
                "channelType": "WebSockets",
                "clientCorrelator": "john rambo rules",
                "applicationTag": "rocky balboa is the best",
            },
            {
                "channelType": "WebSockets",
                "channelLifeTime": 86400,
                "clientCorrelator": "john rambo rules",
                "applicationTag": "rocky balboa is the best",
                "channelData": {
                    "channelURL": "ws://testserver/5/channels/4/ws",
                    "maxNotifications": 7200,
                },
                "id": 4,
            },
            id="type + client correlator + application tag",
        ),
    ],
)
def test_create_notification_channel_success(test_data, expected_data):
    URL_FORMAT, USER_ID = "/{}/channels", 5

    response = client.post(URL_FORMAT.format(USER_ID), json=test_data)

    assert 201 == response.status_code
    assert expected_data == response.json()


def test_list_notification_channel(notification_channel_fabric):
    def assert_channel(db_channel, resp_channel):
        assert db_channel.id == resp_channel["id"]
        assert db_channel.channel_type == resp_channel["channelType"]
        assert db_channel.channel_life_time == resp_channel["channelLifeTime"]
        assert db_channel.client_correlator == resp_channel["clientCorrelator"]
        assert db_channel.application_tag == resp_channel["applicationTag"]
        assert db_channel.channel_data == resp_channel["channelData"]

    URL_FORMAT = "/{}/channels"

    expected_channels = [notification_channel_fabric() for _ in range(10)]

    user_id = expected_channels[0].user_id

    response = client.get(URL_FORMAT.format(user_id))

    assert 200 == response.status_code
    received_channels = response.json()

    for e_channel in expected_channels:
        r_match = [
            channel for channel in received_channels if channel["id"] == e_channel.id
        ].pop()

        assert_channel(e_channel, r_match)


def test_get_notification_channel(notification_channel):
    URL_FORMAT = "/{}/channels/{}"

    expected = {
        "channelType": "WebSockets",
        "channelLifeTime": 3599,
        "clientCorrelator": "123",
        "applicationTag": "myTag",
        "channelData": {"maxNotifications": 10},
        "id": 1,
    }

    response = client.get(
        URL_FORMAT.format(notification_channel.user_id, notification_channel.id)
    )

    assert 200 == response.status_code
    received = response.json()

    assert received == expected


def test_delete_notification_channel(db, notification_channel):
    URL_FORMAT = "/{}/channels/{}"

    response = client.delete(
        URL_FORMAT.format(notification_channel.user_id, notification_channel.id)
    )

    assert 204 == response.status_code
    assert None is get_notification_channel(
        db, notification_channel.user_id, notification_channel.id
    )


def test_get_notification_channel_lifetime(notification_channel):
    URL_FORMAT = "/{}/channels/{}/channelLifetime"

    expected = {"channelLifeTime": notification_channel.channel_life_time}

    response = client.get(
        URL_FORMAT.format(notification_channel.user_id, notification_channel.id)
    )

    assert 200 == response.status_code
    assert expected == response.json()


def test_put_notification_channel_lifetime(notification_channel):
    URL_FORMAT, LIFETIME_IN_SECS = (
        "/{}/channels/{}/channelLifetime",
        100,
    )

    expected = {"channelLifeTime": LIFETIME_IN_SECS}

    response = client.put(
        URL_FORMAT.format(notification_channel.user_id, notification_channel.id),
        json=expected,
    )

    assert 200 == response.status_code
    assert expected == response.json()
