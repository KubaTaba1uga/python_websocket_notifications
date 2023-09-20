from fastapi.testclient import TestClient

from message_store.src.web_app import app

client = TestClient(app)


def test_get_users(db_users):
    response = client.get("/users")
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
        response = client.get(f"/users/{i}")
        assert response.status_code == 200

        json = response.json()

        assert len(json) == 2
