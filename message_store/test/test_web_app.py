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
