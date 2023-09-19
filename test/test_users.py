from fastapi.testclient import TestClient

from notifications_service.web_app import app

client = TestClient(app)


def test_get_users(db_users):
    pass
