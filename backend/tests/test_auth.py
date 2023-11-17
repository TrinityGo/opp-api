from fastapi.testclient import TestClient
from main import app
from routers.auth import create_user, CreateUserRequest
from db.database import SessionLocal

client = TestClient(app)

def setup_module(module):
    # Create a test user
    create_user_request = CreateUserRequest(
        email="test111@example.com",
        username="emelina",
        first_name="emelina",
        surname="Wang",
        password="123ABCabc!",
        role="customer" 
    )
    db = SessionLocal()
    
    create_user(db, create_user_request)

def test_token_generation():
    # Now run your test assuming the user exists
    response = client.post("/auth/token", data={"username": "testuser", "password": "password"})
    assert response.status_code == 401
    assert 'access_token' in response.json()


def test_user_creation():
    response = client.post("/auth/", json={"email": "test@example.com", "password": "password"})
    assert response.status_code == 422


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
    assert response.status_code == 201