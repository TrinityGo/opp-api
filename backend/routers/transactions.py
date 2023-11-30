from fastapi import APIRouter, Depends, HTTPException, Path
from pydantic import BaseModel, Field
from starlette import status
from sqlalchemy.orm import Session
from sqlalchemy import Date, extract, func
from backend.db.database import SessionLocal
from datetime import datetime
from backend.models.models import Transactions
from backend.routers.auth import get_current_user
from backend.routers.helpers import check_user_authentication, encrypt_card_number, process_transaction
from backend.routers.admin import read_all_transactions
from typing import Annotated
from backend.routers.admin import check_admin_user_auth
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
    # transaction_id: int
    # customer_id: int
    merchant_id: int
    customer_bank_info: str
    merchant_bank_info: str
    card_number: str
    amount: float
    time_stamp: datetime
    payment_type: str
        
class UpdateRequest(BaseModel):
    status: str
    # TODO update time_stamp or not?


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_transaction(user: user_dependency, db: db_dependency, request: TransactionRequest):
    check_user_authentication(user)
    
    try:
        encrypted_card_number = encrypt_card_number(request.card_number)
        create_transaction_model = Transactions(
            # transaction_id=request.transaction_id,
            customer_id=user.get('id'),
            merchant_id=request.merchant_id,
            customer_bank_info=request.customer_bank_info,
            merchant_bank_info=request.merchant_bank_info,
            encrypted_card_number=encrypted_card_number,
            time_stamp=request.time_stamp,
            amount=request.amount,
            payment_type=request.payment_type,
            status='pending'
        )

        # insert unprocessed transaction with pending status
        db.add(create_transaction_model)
        db.commit()
        
        # process transaction and update transaction status
        status = process_transaction(request.payment_type, request.card_number, request.amount)
        create_transaction_model.status = status
        db.commit()
        return {"message": "Transaction created successfully"}
    except Exception as e:
        message = str(e)
        return {"message": "Failed to create transaction " + message}


# regular user-get by user_id
@router.get("/transactions/get")
async def get_all_transactions(user: user_dependency, db: db_dependency):
    check_user_authentication(user)
    if(user.get('user_role') == 'customer'):
        return ( db.query(Transactions).filter(Transactions.customer_id == user.get('id')).all() )
    if(user.get('user_role') == 'merchant'):
        return ( db.query(Transactions).filter(Transactions.merchant_id == user.get('id')).all() )
    return read_all_transactions(user, db)

@router.get("/transaction/{transaction_id}", status_code=status.HTTP_200_OK)
async def get_transaction_by_id(user: user_dependency, db: db_dependency, transaction_id: int = Path(gt=-1)):
    check_user_authentication(user)

    filtered_transactions = db.query(Transactions).filter(Transactions.transaction_id == transaction_id)

    if(user.get('user_role') == "customer"):
        transaction_model = (
            filtered_transactions.filter(Transactions.customer_id == user.get('id')).first()
        )
    elif(user.get('user_role') == 'merchant'):
        transaction_model = (
            filtered_transactions.filter(Transactions.merchant_id == user.get('id')).first()
        )
    elif(user.get('user_role') == 'admin'):
        transaction_model = (
            filtered_transactions.first()
        )

    # transaction_model = (
    #     filtered_transactions.filter(Transactions.transaction_id == transaction_id).filter(Transactions.customer_id == user.get('id')).first()
    # )

    if transaction_model is not None:
        return transaction_model
    raise HTTPException(status_code=404, detail='Transaction not found')


@router.get("/transactions/{date}", status_code=status.HTTP_200_OK)
async def get_transactions_by_date(user: user_dependency, db: db_dependency, date: str = Path(..., description="Date in ISO format")):
    try:
        parsed_date = datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        return {"error": "Invalid date format. Please provide date in YYYY-MM-DD format."}
    
    message = parsed_date.date()
    check_user_authentication(user)

    # try:
    if(user.get('user_role') == "customer"):
        filtered_transactions = db.query(Transactions).filter(Transactions.customer_id == user.get('id'))
    elif(user.get('user_role') == 'merchant'):
        filtered_transactions = db.query(Transactions).filter(Transactions.merchant_id == user.get('id'))
    elif(user.get('user_role') == 'admin'):
        filtered_transactions = db.query(Transactions)
    
    
    transaction_model = (
        filtered_transactions.filter(extract('year', Transactions.time_stamp) == parsed_date.year).filter(extract('month', Transactions.time_stamp) == parsed_date.month).filter(extract('day', Transactions.time_stamp) == parsed_date.day).all()
    )
    # except Exception as e:
    #     return {"message": str(e)}

    if transaction_model is not None:
        return transaction_model
    raise HTTPException(status_code=404, detail=f'Transaction not found on the date: {date}')


@router.get("/transactions/{start_date}/{end_date}", status_code=status.HTTP_200_OK)
async def get_transactions_by_period(user: user_dependency, db: db_dependency, start_date: str = Path(..., description="Start Date in ISO format"), end_date: str = Path(..., description="End Date in ISO format")):
    try:
        parsed_start_date = datetime.strptime(start_date, "%Y-%m-%d")
        parsed_end_date = datetime.strptime(end_date, "%Y-%m-%d") # or user timedelta(days=1)
    except ValueError:
        return {"error": "Invalid date format. Please provide date in YYYY-MM-DD format."}
    
    check_user_authentication(user)

    if(user.get('user_role') == "customer"):
        filtered_transactions = db.query(Transactions).filter(Transactions.customer_id == user.get('id'))
    elif(user.get('user_role') == 'merchant'):
        filtered_transactions = db.query(Transactions).filter(Transactions.merchant_id == user.get('id'))
    elif(user.get('user_role') == 'admin'):
        filtered_transactions = db.query(Transactions)

    transaction_model = (
        filtered_transactions.filter(extract('year', Transactions.time_stamp) >= parsed_start_date.year).filter(extract('month', Transactions.time_stamp) >= parsed_start_date.month).filter(extract('day', Transactions.time_stamp) >= parsed_start_date.day).filter(extract('year', Transactions.time_stamp) <= parsed_end_date.year).filter(extract('month', Transactions.time_stamp) <= parsed_end_date.month).filter(extract('day', Transactions.time_stamp) <= parsed_end_date.day).all()
    )
    # transaction_model = (
    #     db.query(Transactions).filter(Transactions.customer_id == user.get('id')).filter(extract('year', Transactions.time_stamp) >= parsed_start_date.year).filter(extract('month', Transactions.time_stamp) >= parsed_start_date.month).filter(extract('day', Transactions.time_stamp) >= parsed_start_date.day).filter(extract('year', Transactions.time_stamp) <= parsed_end_date.year).filter(extract('month', Transactions.time_stamp) <= parsed_end_date.month).filter(extract('day', Transactions.time_stamp) <= parsed_end_date.day).all()
    # )

    if transaction_model is not None:
        return transaction_model
    raise HTTPException(status_code=404, detail=f'Transaction not found from {start_date} to {end_date}')


@router.get("/balance", status_code=status.HTTP_200_OK)
async def get_balance_sum(user: user_dependency, db: db_dependency):
    check_user_authentication(user)

    if(user.get('user_role') == "customer"):
        filtered_transactions = db.query(Transactions).filter(Transactions.customer_id == user.get('id'))
    elif(user.get('user_role') == 'merchant'):
        filtered_transactions = db.query(Transactions).filter(Transactions.merchant_id == user.get('id'))
    elif(user.get('user_role') == 'admin'):
        filtered_transactions = db.query(Transactions)

    transaction_model = (
        filtered_transactions.filter(func.lower(Transactions.status) == "completed").all()
    )

    if transaction_model is not None:
        balance = sum(transaction.amount for transaction in transaction_model)
        return balance
    raise HTTPException(status_code=404, detail=f'Transaction not found from {start_date} to {end_date}')


@router.get("/balance/{date}", status_code=status.HTTP_200_OK)
async def get_balance_sum_by_date(user: user_dependency, db: db_dependency, date: str = Path(..., description="Date in ISO format")):
    try:
        parsed_date = datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        return {"error": "Invalid date format. Please provide date in YYYY-MM-DD format."}
    
    check_user_authentication(user)


    if(user.get('user_role') == "customer"):
        filtered_transactions = db.query(Transactions).filter(Transactions.customer_id == user.get('id'))
    elif(user.get('user_role') == 'merchant'):
        filtered_transactions = db.query(Transactions).filter(Transactions.merchant_id == user.get('id'))
    elif(user.get('user_role') == 'admin'):
        filtered_transactions = db.query(Transactions)

    transaction_model = (
        filtered_transactions.filter(extract('year', Transactions.time_stamp) == parsed_date.year).filter(extract('month', Transactions.time_stamp) == parsed_date.month).filter(extract('day', Transactions.time_stamp) == parsed_date.day).filter(func.lower(Transactions.status) == "completed").all()
    )

    if transaction_model is not None:
        balance = sum(transaction.amount for transaction in transaction_model)
        return balance
    raise HTTPException(status_code=404, detail=f'Transaction not found on the date: {date}')


@router.get("/balance/{start_date}/{end_date}", status_code=status.HTTP_200_OK)
async def get_balance_sum_by_period(user: user_dependency, db: db_dependency, start_date: str = Path(..., description="Start Date in ISO format"), end_date: str = Path(..., description="End Date in ISO format")):
    try:
        parsed_start_date = datetime.strptime(start_date, "%Y-%m-%d")
        parsed_end_date = datetime.strptime(end_date, "%Y-%m-%d") # or user timedelta(days=1)
    except ValueError:
        return {"error": "Invalid date format. Please provide date in YYYY-MM-DD format."}
    
    check_user_authentication(user)


    if(user.get('user_role') == "customer"):
        filtered_transactions = db.query(Transactions).filter(Transactions.customer_id == user.get('id'))
    elif(user.get('user_role') == 'merchant'):
        filtered_transactions = db.query(Transactions).filter(Transactions.merchant_id == user.get('id'))
    elif(user.get('user_role') == 'admin'):
        filtered_transactions = db.query(Transactions)

    transaction_model = (
        filtered_transactions.filter(extract('year', Transactions.time_stamp) >= parsed_start_date.year).filter(extract('month', Transactions.time_stamp) >= parsed_start_date.month).filter(extract('day', Transactions.time_stamp) >= parsed_start_date.day).filter(extract('year', Transactions.time_stamp) <= parsed_end_date.year).filter(extract('month', Transactions.time_stamp) <= parsed_end_date.month).filter(extract('day', Transactions.time_stamp) <= parsed_end_date.day).filter(func.lower(Transactions.status) == "completed").all()
    )

    if transaction_model is not None:
        balance = sum(transaction.amount for transaction in transaction_model)
        return balance
    raise HTTPException(status_code=404, detail=f'Transaction not found from {start_date} to {end_date}')


# admin can update transaction by transaction_id
@router.put("/transaction/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_transaction_by_id(user: user_dependency, db: db_dependency,
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


# System will auto check and update all approved transaction when they are completed
# No user authentication needed
@router.put("/transactions/update", status_code=status.HTTP_204_NO_CONTENT)
async def auto_update_transaction(db: db_dependency):
    # TODO May be auto-updating depending on payment processing
    transaction_model = (
        db.query(Transactions).filter(Transactions.status == "approved").all()
    )

    # check_user_authentication(user)
    if transaction_model is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    # make the updates
    time_stamp = datetime.now()
    for transaction in transaction_model:
        if(time_stamp.year >= transaction.time_stamp.year & time_stamp.month >= transaction.time_stamp.month & (time_stamp.day >= transaction.time_stamp.day+2)):
            transaction.status = "completed"
    db.commit()


@router.delete("/transaction/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_transaction(user: user_dependency, db: db_dependency, transaction_id: int = Path(gt=-1)):
    check_admin_user_auth(user)

    filtered_transactions = db.query(Transactions).filter(Transactions.transaction_id == transaction_id)
    
    if(user.get('user_role') == "customer"):
        transaction_model = filtered_transactions.filter(Transactions.customer_id == user.get('id')).first()
    elif(user.get('user_role') == 'merchant'):
        transaction_model = filtered_transactions.filter(Transactions.merchant_id == user.get('id')).first()
    elif(user.get('user_role') == 'admin'):
        filtered_transactions = filtered_transactions.first()

    # transaction_model = db.query(Transactions).filter(Transactions.transaction_id == transaction_id).filter(Transactions.customer_id == user.get('id')).first()
    
    if transaction_model is None:
        raise HTTPException(status_code=404, detail='Transaction not found')

    db.query(Transactions).filter(Transactions.transaction_id == transaction_id).filter(Transactions.customer_id == user.get('id')).delete()
    db.commit()
