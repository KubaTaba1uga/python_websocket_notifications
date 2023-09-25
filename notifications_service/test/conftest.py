import os
import sys

import pytest
from sqlalchemy.sql import text

from notifications_service.src.db_models import create_notification_channel
from notifications_service.src.db_models import NotificationChannel
from notifications_service.src.db_models import save_obj
from notifications_service.src.schemas import NotificationChannelUserSchema
from shared.database import get_db
from shared.db_models import Message

# Make sure that the application source directory (this directory's parent) is
# on sys.path.

app_root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, app_root_dir)


@pytest.fixture(autouse=False)
def db():
    for db_local in get_db():
        db_cleanup(db_local)

        yield db_local

        db_cleanup(db_local)


def db_cleanup(db_local):
    def delete_table_records(db_local, table):
        db_local.execute(text(f"TRUNCATE {table}"))

    def reset_table_counter(db_local, table):
        db_local.execute(text(f"ALTER SEQUENCE {table}_id_seq RESTART WITH 1"))

    tables_to_teardown = [NotificationChannel.__tablename__, Message.__tablename__]

    for table in tables_to_teardown:
        delete_table_records(db_local, table)
        reset_table_counter(db_local, table)

    db_local.commit()


@pytest.fixture
def notification_channel_fabric(db):
    def local_fabric(
        user_id=5,
        type="WebSockets",
        life_time=3600,
        cc="123",
        at="myTag",
        cd={
            "maxNotifications": 10,
        },
    ):
        nc = NotificationChannelUserSchema(
            channelType=type,
            channelLifeTime=life_time,
            clientCorrelator=cc,
            applicationTag=at,
            channelData=cd,
        )

        save_obj(db, db_nc := create_notification_channel(db, user_id, nc))
        return db_nc

    return local_fabric


@pytest.fixture
def notification_channel(notification_channel_fabric):
    return notification_channel_fabric(
        5,
        "WebSockets",
        3600,
        "123",
        "myTag",
        {
            "maxNotifications": 10,
        },
    )
