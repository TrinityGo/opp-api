from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from starlette import status
from sqlalchemy.orm import Session
from db.database import SessionLocal
from datetime import datetime
from models.models import Transactions
from routers.auth import get_current_user
from routers.helpers import check_user_authentication, encrypt_transaction_info, process_transaction
from typing import Annotated
import json

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependency = Annotated[Session, Depends(get_db)]

# when an API uses this, it will enforce authorization
user_dependency = Annotated[dict, (Depends(get_current_user))]


class CreateTransactionRequest(BaseModel):
    transaction_id: int
    customer_id: int
    merchant_id: int
    customer_bank_info: str
    merchant_bank_info: str
    amount: float
    time_stamp: datetime
        
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_transaction(user: user_dependency, db: db_dependency, request: CreateTransactionRequest):
    check_user_authentication(user)
    
    encrypted_transaction_info = encrypt_transaction_info(request.customer_bank_info, request.merchant_bank_info)
    transaction_data = dict()
    transaction_data['transaction_id'] = request.transaction_id
    transaction_data['customer_id'] = user.get('id')
    transaction_data['merchant_id'] = request.merchant_id
    transaction_data['encrypted_info'] = json.dumps(encrypted_transaction_info)  
    transaction_data['time_stamp'] = request.time_stamp
    transaction_data['status'] = 'pending'
    transaction_model = Transactions(**transaction_data)

    # insert unprocessed transaction with pending status
    db.add(transaction_model)
    db.commit()
    
    # process transaction and update transaction status
    status = process_transaction(transaction_model)
    transaction_model.status = status
    db.add(transaction_model)
    db.commit()


@router.get("/read-all")
async def get_all(user: user_dependency, db: db_dependency):
    check_user_authentication(user)
    return db.query(Transactions).filter(Transactions.customer_id == user.get('id')).all()


@router.get("/transaction/{transaction_id}", status_code=status.HTTP_200_OK)
async def get_transaction_by_id(user: user_dependency, db: db_dependency, transaction_id: int = Path(gt=0)):
    check_user_authentication(user)

    transaction_model = (
        db.query(Transactions).filter(Transactions.transaction_id == transaction_id).filter(Transactions.customer_id == user.get('id')).first()
    )

    if transaction_model is not None:
        return transaction_model
    raise HTTPException(status_code=404, detail='Transaction not found')


@router.get("/transaction/{date}", status_code=status.HTTP_200_OK)
async def get_transaction_by_date(user: user_dependency, db: db_dependency, date: datetime = Path(..., description="Date in ISO format"):
    check_user_authentication(user)

    transaction_model = (
        db.query(Transactions).filter(Transactions.transaction_id == transaction_id).filter(Transactions.customer_id == user.get('id')).first()
    )

    if transaction_model is not None:
        return transaction_model
    raise HTTPException(status_code=404, detail='Transaction not found')