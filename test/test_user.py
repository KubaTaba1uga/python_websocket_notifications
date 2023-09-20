import requests
from fastapi.testclient import TestClient

APP_URL = "http://127.0.0.1"
MESSAGE_STORE__URL = APP_URL + ":80"


def test_get_users(db_users):
    response = requests.get(MESSAGE_STORE__URL + "/users")
    assert response.status_code == 200

    json = response.json()

    assert len(json) == 5
    for user in json:
        assert any(
            user["id"] == db_user.id and user["username"] == db_user.username
            for db_user in db_users
        )


def test_get_user(db_users):
    for i in range(1, 5):
        response = requests.get(MESSAGE_STORE__URL + f"/users/{i}")
        assert response.status_code == 200

        json = response.json()

        assert len(json) == 2
