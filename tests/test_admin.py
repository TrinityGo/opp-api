"""
Tests for the admin routes
"""
# Standard imports
from fastapi.testclient import TestClient
from backend.main import app

# Test client
client = TestClient(app)

def test_admin_transactions():
    """Test admin transactions"""
    response = client.get("/admin/transactions")
    assert response.status_code == 401

def test_admin_users():
    """Test admin users"""
    response = client.get("/admin/users")
    assert response.status_code == 401