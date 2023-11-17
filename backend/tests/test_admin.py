from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_admin_transactions():
    response = client.get("/admin/transactions")
    assert response.status_code == 200  # Assuming public access for simplicity

def test_admin_users():
    response = client.get("/admin/users")
    assert response.status_code == 200
