from fastapi import APIRouter, Depends, HTTPException, Path
from pydantic import BaseModel, Field
from starlette import status
from sqlalchemy.orm import Session
from sqlalchemy import Date, extract, func
from db.database import SessionLocal
from datetime import datetime
from models.models import Transactions
from routers.auth import get_current_user
from routers.helpers import check_user_authentication, encrypt_transaction_info, process_transaction
from typing import Annotated
from routers.admin import check_admin_user_auth
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


class TransactionRequest(BaseModel):
    transaction_id: int
    # TODO customer_id: int
    merchant_id: int
    customer_bank_info: str
    merchant_bank_info: str
    amount: float
    time_stamp: datetime
        
class UpdateRequest(BaseModel):
    status: str
    # TODO update time_stamp or not?


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_transaction(user: user_dependency, db: db_dependency, request: TransactionRequest):
    check_user_authentication(user)
    
    try:
        encrypted_transaction_info = encrypt_transaction_info(request.customer_bank_info, request.merchant_bank_info)
        transaction_data = dict()
        transaction_data['transaction_id'] = request.transaction_id
        transaction_data['customer_id'] = user.get('id')
        transaction_data['merchant_id'] = request.merchant_id
        transaction_data['encrypted_info'] = encrypted_transaction_info
        # json.dumps(encrypted_transaction_info)  
        transaction_data['time_stamp'] = request.time_stamp
        transaction_data['amount'] = request.amount
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

        return {"message": "Transaction created successfully"}
    except Exception as e:
        message = str(e)
        return {"message": "Failed to create transaction" + message}

# regular user-get by user_id
@router.get("/get-all")
async def get_all(user: user_dependency, db: db_dependency):
    check_user_authentication(user)
    return db.query(Transactions).filter(Transactions.customer_id == user.get('id')).all()


@router.get("/transaction/{transaction_id}", status_code=status.HTTP_200_OK)
async def get_transaction_by_id(user: user_dependency, db: db_dependency, transaction_id: int = Path(gt=-1)):
    check_user_authentication(user)

    transaction_model = (
        db.query(Transactions).filter(Transactions.transaction_id == transaction_id).filter(Transactions.customer_id == user.get('id')).first()
    )

    if transaction_model is not None:
        return transaction_model
    raise HTTPException(status_code=404, detail='Transaction not found')


@router.get("/transactions/{date}", status_code=status.HTTP_200_OK)
async def get_transaction_by_date(user: user_dependency, db: db_dependency, date: str = Path(..., description="Date in ISO format")):
    try:
        parsed_date = datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        return {"error": "Invalid date format. Please provide date in YYYY-MM-DD format."}
    
    message = parsed_date.date()
    check_user_authentication(user)

    try:
        transaction_model = (
            db.query(Transactions).filter(Transactions.customer_id == user.get('id')).filter(extract('year', Transactions.time_stamp) == parsed_date.year).filter(extract('month', Transactions.time_stamp) == parsed_date.month).filter(extract('day', Transactions.time_stamp) == parsed_date.day).all()
        )
    except Exception as e:
        return {"message": str(e)}

    if transaction_model is not None:
        return transaction_model
    raise HTTPException(status_code=404, detail=f'Transaction not found on the date: {date}')


@router.get("/transactions/{start_date}/{end_date}", status_code=status.HTTP_200_OK)
async def get_transaction_by_period(user: user_dependency, db: db_dependency, start_date: str = Path(..., description="Start Date in ISO format"), end_date: str = Path(..., description="End Date in ISO format")):
    try:
        parsed_start_date = datetime.strptime(start_date, "%Y-%m-%d")
        parsed_end_date = datetime.strptime(end_date, "%Y-%m-%d") # or user timedelta(days=1)
    except ValueError:
        return {"error": "Invalid date format. Please provide date in YYYY-MM-DD format."}
    
    check_user_authentication(user)

    transaction_model = (
        db.query(Transactions).filter(Transactions.customer_id == user.get('id')).filter(extract('year', Transactions.time_stamp) >= parsed_start_date.year).filter(extract('month', Transactions.time_stamp) >= parsed_start_date.month).filter(extract('day', Transactions.time_stamp) >= parsed_start_date.day).filter(extract('year', Transactions.time_stamp) <= parsed_end_date.year).filter(extract('month', Transactions.time_stamp) <= parsed_end_date.month).filter(extract('day', Transactions.time_stamp) <= parsed_end_date.day).all()
    )

    if transaction_model is not None:
        return transaction_model
    raise HTTPException(status_code=404, detail=f'Transaction not found from {start_date} to {end_date}')


@router.get("/balance", status_code=status.HTTP_200_OK)
async def get_balance(user: user_dependency, db: db_dependency):
    check_user_authentication(user)

    transaction_model = (
        db.query(Transactions).filter(Transactions.merchant_id == user.get('id')).filter(func.lower(Transactions.status) == "completed").all()
    )

    if transaction_model is not None:
        balance = sum(transaction.amount for transaction in transaction_model)
        return balance
    raise HTTPException(status_code=404, detail=f'Transaction not found from {start_date} to {end_date}')


@router.get("/balance/{date}", status_code=status.HTTP_200_OK)
async def get_balance_by_date(user: user_dependency, db: db_dependency, date: str = Path(..., description="Date in ISO format")):
    try:
        parsed_date = datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        return {"error": "Invalid date format. Please provide date in YYYY-MM-DD format."}
    
    check_user_authentication(user)

    transaction_model = (
        db.query(Transactions).filter(Transactions.merchant_id == user.get('id')).filter(extract('year', Transactions.time_stamp) == parsed_date.year).filter(extract('month', Transactions.time_stamp) == parsed_date.month).filter(extract('day', Transactions.time_stamp) == parsed_date.day).filter(func.lower(Transactions.status) == "completed").all()
    )

    if transaction_model is not None:
        balance = sum(transaction.amount for transaction in transaction_model)
        return balance
    raise HTTPException(status_code=404, detail=f'Transaction not found on the date: {date}')


@router.get("/balance/{start_date}/{end_date}", status_code=status.HTTP_200_OK)
async def get_balance_by_period(user: user_dependency, db: db_dependency, start_date: str = Path(..., description="Start Date in ISO format"), end_date: str = Path(..., description="End Date in ISO format")):
    try:
        parsed_start_date = datetime.strptime(start_date, "%Y-%m-%d")
        parsed_end_date = datetime.strptime(end_date, "%Y-%m-%d") # or user timedelta(days=1)
    except ValueError:
        return {"error": "Invalid date format. Please provide date in YYYY-MM-DD format."}
    
    check_user_authentication(user)

    transaction_model = (
        db.query(Transactions).filter(Transactions.merchant_id == user.get('id')).filter(extract('year', Transactions.time_stamp) >= parsed_start_date.year).filter(extract('month', Transactions.time_stamp) >= parsed_start_date.month).filter(extract('day', Transactions.time_stamp) >= parsed_start_date.day).filter(extract('year', Transactions.time_stamp) <= parsed_end_date.year).filter(extract('month', Transactions.time_stamp) <= parsed_end_date.month).filter(extract('day', Transactions.time_stamp) <= parsed_end_date.day).filter(func.lower(Transactions.status) == "completed").all()
    )

    if transaction_model is not None:
        balance = sum(transaction.amount for transaction in transaction_model)
        return balance
    raise HTTPException(status_code=404, detail=f'Transaction not found from {start_date} to {end_date}')


@router.put("/transaction/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_transaction(user: user_dependency, db: db_dependency,
                      request: UpdateRequest,
                      transaction_id: int = Path(gt=-1)):
    # TODO May be auto-updating depending on payment processing
    # check_user_authentication(user)
    check_admin_user_auth(user)

    transaction_model = db.query(Transactions).filter(Transactions.transaction_id == transaction_id).first()

    if transaction_model is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    # make the updates
    transaction_model.status = request.status
    db.commit()


@router.delete("/transaction/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_transaction(user: user_dependency, db: db_dependency, transaction_id: int = Path(gt=-1)):
    check_admin_user_auth(user)

    transaction_model = db.query(Transactions).filter(Transactions.transaction_id == transaction_id).filter(Transactions.customer_id == user.get('id')).first()
    
    if transaction_model is None:
        raise HTTPException(status_code=404, detail='Transaction not found')

    db.query(Transactions).filter(Transactions.transaction_id == transaction_id).filter(Transactions.customer_id == user.get('id')).delete()
    db.commit()