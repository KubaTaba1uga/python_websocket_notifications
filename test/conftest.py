import pytest

from notifications_service.test.conftest import db
from notifications_service.test.conftest import notification_channel_fabric
from shared.database import get_db
from shared.db_models import get_users


@pytest.fixture
def db_users():
    db = list(get_db()).pop()
    return get_users(db)
