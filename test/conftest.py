import pytest

from notifications_service.web_app import get_db
from shared import user as db_user


@pytest.fixture
def db_users():
    db = list(get_db()).pop()
    return db_user.get_users(db)
