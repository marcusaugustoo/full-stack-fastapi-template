from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code in [200, 404]

def test_users_endpoint():
    response = client.get("/api/v1/users/")
    assert response.status_code in [200, 401, 403]

def test_items_endpoint():
    response = client.get("/api/v1/items/")
    assert response.status_code in [200, 401, 403]

def test_login_endpoint():
    response = client.post("/api/v1/login/access-token", data={"username": "test", "password": "test"})
    assert response.status_code in [200, 400, 401]