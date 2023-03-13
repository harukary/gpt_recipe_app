from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

def test_create_item():
    response = client.post(
        "/items/",
        json={"name": "test", "price": 1.0, "is_offer": True}
    )
    assert response.status_code == 200
    assert response.json() == {"name": "test", "price": 1.0, "is_offer": True}