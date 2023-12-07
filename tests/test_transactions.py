"""Test the transactions endpoints"""
# Standard imports
from fastapi.testclient import TestClient
from backend.main import app

# Test client
client = TestClient(app)


def test_get_transactions():
    """Test get transactions."""
    response = client.get("/transactions/get")
    assert response.status_code == 401

def test_create_transaction():
    """Test create transaction."""
    transaction_data = {
        "merchant_id": 1,
        "customer_bank_info": "bank_info",
        "merchant_bank_info": "merchant_bank_info",
        "card_number": "1234567890123456",
        "amount": 100.0,
        "time_stamp": "2023-01-01T00:00:00",
        "payment_type": "credit_card"
    }
    response = client.post("/transactions/", json=transaction_data)
    assert response.status_code == 404

def test_get_transaction_by_id():
    """Test get transaction by id."""
    response = client.get("/transactions/transaction/1")
    assert response.status_code == 401
