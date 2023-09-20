import pytest

from shared.database import get_db
from shared.db_models import get_users


@pytest.fixture
def db_users():
    db = list(get_db()).pop()
    return get_users(db)
