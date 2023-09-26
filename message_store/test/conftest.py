import os
import sys

import pytest

from notifications_service.test.conftest import db
from shared.db_models import create_messge
from shared.db_models import create_subscription
from shared.db_models import Message
from shared.db_models import save_obj
from shared.db_models import Subscription
from shared.schemas import MessageUserSchema
from shared.schemas import SubscriptionUserSchema

# Make sure that the application source directory (this directory's parent) is
# on sys.path.

app_root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, app_root_dir)


@pytest.fixture
def message_fabric(db):
    def local_fabric(sender_id: int, receiver_id: int, content_str: str) -> Message:
        msg_schema = MessageUserSchema(
            from_=sender_id, to=receiver_id, content=content_str
        )

        save_obj(db, msg_obj := create_messge(db, msg_schema))

        return msg_obj

    return local_fabric


@pytest.fixture
def message(message_fabric):
    return message_fabric(1, 2, "Hi")


@pytest.fixture
def subscription_fabric(db):
    USER_ID = 1

    def local_fabric(
        user_id: int = USER_ID,
        callback_reference: dict = {"notifyURL": "http://localhost/proxy"},
        filter: str = "*",
        client_correlator: str = f"ws://localhost/channels/{USER_ID}/ws",
    ) -> Subscription:
        sub_schema = SubscriptionUserSchema(
            callback_reference=callback_reference,
            filter=filter,
            client_correlator=client_correlator,
        )

        save_obj(db, sub_obj := create_subscription(db, user_id, sub_schema))

        return sub_obj

    return local_fabric


@pytest.fixture
def subscription(subscription_fabric):
    return subscription_fabric()


# @pytest.fixture
# def notification_channel(notification_channel_fabric):
#     return notification_channel_fabric(
#         5,
#         "WebSockets",
#         3600,
#         "123",
#         "myTag",
#         {
#             "maxNotifications": 10,
#         },
#     )
