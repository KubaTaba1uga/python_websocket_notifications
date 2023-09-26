from datetime import datetime
from unittest.mock import patch

from shared import db_models
from shared import schemas


def test_get_message(db, message):
    msg_obj = db_models.get_message(db, message.id)

    assert isinstance(msg_obj, db_models.Message)
    assert message.from_ == msg_obj.from_
    assert message.to == msg_obj.to
    assert message.content == msg_obj.content
    assert message.id == msg_obj.id


def test_create_msg(db):
    msg_schema = schemas.MessageUserSchema(from_=1, to=2, content="Hi")

    saved_msg = db_models.create_messge(db, msg_schema)
    db_models.save_obj(db, saved_msg)

    msg_obj = db_models.get_message(db, saved_msg.id)

    assert msg_schema.from_ == msg_obj.from_
    assert msg_schema.to == msg_obj.to
    assert msg_schema.content == msg_obj.content
    assert isinstance(msg_obj.id, int)


def test_create_subscription(db):
    USER_ID = 1

    sub_schema = schemas.SubscriptionUserSchema(
        callback_reference={"notifyURL": "http://localhost/proxy"},
    )

    now = datetime(2000, 6, 6, 0, 0, 0)

    with patch(
        "shared.spec_utils.channel_life_time_utils.datetime",
    ) as mocked_datetime:
        mocked_datetime.now = lambda: now

        sub_db = db_models.create_subscription(db, USER_ID, sub_schema)

    assert USER_ID == sub_db.user_id
    assert sub_schema.callback_reference == sub_db.callback_reference
    assert sub_schema.filter == sub_db.filter
    assert sub_schema.client_correlator == sub_db.client_correlator
    assert 0 == sub_db.index
    assert None is sub_db.restart_token
    assert datetime(2000, 6, 7, 0, 0) == sub_db.expiry_date_time


def test_get_subscription(db, subscription):
    sub_db = db_models.get_subscription(db, subscription.user_id, subscription.id)

    assert subscription.user_id == sub_db.user_id
    assert subscription.callback_reference == sub_db.callback_reference
    assert subscription.filter == sub_db.filter
    assert subscription.client_correlator == sub_db.client_correlator
    assert subscription.index == sub_db.index
    assert subscription.restart_token == sub_db.restart_token
    assert subscription.expiry_date_time == sub_db.expiry_date_time


def test_list_subscriptions(db, subscription_fabric):
    SUBS_AMOUNT = 10

    subscriptions_list = [subscription_fabric() for _ in range(SUBS_AMOUNT)]

    sub = subscriptions_list[0]

    received = db_models.list_subscriptions(db, sub.user_id)

    assert SUBS_AMOUNT == len(received)
    assert all(
        any(exp_c.id == rec_c.id for rec_c in received) for exp_c in subscriptions_list
    )
