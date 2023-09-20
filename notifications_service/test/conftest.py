import os
import sys

import pytest

from shared.database import get_db
from shared.db_models import get_users

# Make sure that the application source directory (this directory's parent) is
# on sys.path.

app_root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, app_root_dir)


@pytest.fixture
def db():
    return list(get_db()).pop()
