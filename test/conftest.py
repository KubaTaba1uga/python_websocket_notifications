import pytest

from shared import user as db_user
from shared.database import get_db


@pytest.fixture
def db_users():
    db = list(get_db()).pop()
    return db_user.get_users(db)
