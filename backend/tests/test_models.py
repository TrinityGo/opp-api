from db.database import SessionLocal
from models.models import Users, Transactions

def test_model_creation():
    session = SessionLocal()
    new_user = Users(email="test@example.com", username="testuser")
    session.add(new_user)
    session.commit()

    retrieved_user = session.query(Users).filter_by(username="testuser").first()
    assert retrieved_user is not None
    assert retrieved_user.email == "test@example.com"