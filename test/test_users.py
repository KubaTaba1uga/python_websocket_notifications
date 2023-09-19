from src.web_app import app

client = TestClient(app)

def test_get_users(app_users)
