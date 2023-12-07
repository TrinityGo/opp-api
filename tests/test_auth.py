from fastapi.testclient import TestClient
from backend.main import app
from backend.routers.auth import create_user, CreateUserRequest
from backend.db.database import SessionLocal

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


def test_user_creation():
    response = client.post("/auth/", json={"email": "test@example.com", "password": "password"})
    assert response.status_code == 422


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