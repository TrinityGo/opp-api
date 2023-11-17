from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_user_creation():
    response = client.post("/auth/", json={"email": "test@example.com", "password": "password"})
    assert response.status_code == 401

def test_token_generation():
    response = client.post("/auth/token", data={"username": "testuser", "password": "password"})
    assert response.status_code == 401
    assert "access_token" in response.json()

def test_user_authentication():
    response = client.post("/auth/token", data={"username": "testuser", "password": "testpassword"})
    assert response.status_code == 401
    assert "access_token" in response.json()
    # Save the token if needed for subsequent tests

def test_create_user():
    user_data = {
        "email": "newuser@example.com",
        "username": "newuser",
        "first_name": "New",
        "surname": "User",
        "password": "newpassword",
        "role": "customer"
    }
    response = client.post("/auth/", json=user_data)
    assert response.status_code == 401