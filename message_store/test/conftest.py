import os
import sys

import pytest

from shared import user as db_user
from shared.database import get_db

# Make sure that the application source directory (this directory's parent) is
# on sys.path.

app_root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, app_root_dir)


@pytest.fixture
def db_users():
    db = list(get_db()).pop()
    return db_user.get_users(db)
