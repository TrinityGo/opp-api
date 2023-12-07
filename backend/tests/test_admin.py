from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_admin_transactions():
    response = client.get("/admin/transactions")
    assert response.status_code == 401

def test_admin_users():
    response = client.get("/admin/users")
    assert response.status_code == 401
