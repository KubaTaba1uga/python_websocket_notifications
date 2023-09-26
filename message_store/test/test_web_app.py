from copy import copy

import pytest
from fastapi.testclient import TestClient

from message_store.src.web_app import app
from shared.db_models import get_message

client = TestClient(app)


def assert_message(msg_db, msg_reciv):
    assert msg_db.from_ == msg_reciv["from_"]
    assert msg_db.to == msg_reciv["to"]
    assert msg_db.content == msg_reciv["content"]
    assert msg_db.id == msg_reciv["id"]


def assert_subscription(sub_db, sub_reciv):
    assert sub_db.id == sub_reciv["id"]
    assert sub_db.callback_reference == sub_reciv["callbackReference"]
    assert sub_db.filter == sub_reciv["filter"]
    assert sub_db.client_correlator == sub_reciv["clientCorrelator"]
    assert sub_db.index == sub_reciv["index"]
    assert sub_db.restart_token == sub_reciv["restartToken"]
    assert sub_db.max_events == sub_reciv["maxEvents"]


def test_create_message_success():
    msg_data = {"from_": 1, "to": 2, "content": "I like cats and frogs."}
    response = client.post("/messages", json=msg_data)

    assert 200 == response.status_code

    received_msg = response.json()
    msg_data["id"] = received_msg["id"]

    assert msg_data == received_msg


def test_list_message_success(message_fabric):
    MESSAGES_NO = 10

    msg_data = {
        "sender_id": 1,
        "receiver_id": 2,
        "content_str": "I like cats and frogs.",
    }

    messages = [message_fabric(**msg_data) for _ in range(MESSAGES_NO)]

    response = client.get("/messages")

    assert 200 == response.status_code
    received_msgs = response.json()

    assert len(received_msgs) == MESSAGES_NO
    for i in range(MESSAGES_NO):
        assert_message(messages[i], received_msgs[i])


def test_get_message_success(message_fabric):
    MESSAGES_NO = 10

    msg_data = {
        "sender_id": 1,
        "receiver_id": 2,
        "content_str": "I like cats and frogs.",
    }

    messages = [message_fabric(**msg_data) for _ in range(MESSAGES_NO)]

    for message in messages:
        response = client.get(f"/messages/{message.id}")
        assert 200 == response.status_code
        assert_message(message, response.json())


def test_create_subscription_success():
    subscription_data, user_id = {
        "callback_reference": {"notifyURL": "http://localhost/proxy"}
    }, 1

    expected_data = {
        "callbackReference": subscription_data["callback_reference"],
        "clientCorrelator": None,
        "duration": 86400,
        "filter": "** dummy filter **",
        "maxEvents": 100,
        "restartToken": "dummy restart token",
        "index": 0,
        "id": 1,
    }

    response = client.post(f"/{user_id}/subscriptions", json=subscription_data)

    assert 201 == response.status_code

    received_subscription = response.json()

    assert expected_data == received_subscription


def test_list_subscription_success(subscription_fabric):
    SUBSCRIPTIONS_NO = 10

    subscriptions = [subscription_fabric() for _ in range(SUBSCRIPTIONS_NO)]

    random_sub = subscriptions[0]

    response = client.get(f"/{random_sub.user_id}/subscriptions")

    assert 200 == response.status_code
    received_subscriptions = response.json()

    assert len(received_subscriptions) == SUBSCRIPTIONS_NO
    for i in range(SUBSCRIPTIONS_NO):
        assert_subscription(subscriptions[i], received_subscriptions[i])


def test_get_subscription_success(subscription):
    subscription_id, user_id = subscription.id, 1

    response = client.get(f"/{user_id}/subscriptions/{subscription_id}")

    assert 200 == response.status_code

    received_subscription = response.json()

    assert_subscription(subscription, received_subscription)
