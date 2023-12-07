from fastapi.testclient import TestClient
from backend.src.main import app

client = TestClient(app)

def test_create_transaction():
    response = client.post("/transactions/", json={"merchant_id": 1, "amount": 100.0})
    assert response.status_code == 404 

def test_get_transactions():
    response = client.get("/transactions/get")
    assert response.status_code == 401
    
def test_create_transaction():
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
    # Validate the response

def test_get_transaction_by_id():
    response = client.get("/transactions/transaction/1")
    assert response.status_code == 401