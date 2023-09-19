from fastapi.testclient import TestClient
from src.web_app import app

client = TestClient(app)


def test_get_users(app_users):
    pass
