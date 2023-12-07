"""This module is responsible for handling all the transaction related
routes and functions. It defines routes for creating, reading, updating,
and deleting transactions, as well as routes for retrieving transaction
information. It also defines functions for processing transactions and
encrypting and decrypting card numbers."""
# Standard imports
from datetime import datetime
from typing import Annotated
# Third-party imports
from fastapi import APIRouter, Depends, HTTPException, Path
from pydantic import BaseModel
from starlette import status
from sqlalchemy.orm import Session
from sqlalchemy import extract, func, or_
from backend.db.database import SessionLocal
# Local imports
from backend.models.models import Transactions
from backend.routers.auth import get_current_user
from backend.routers.helpers import check_user_authentication, \
                                    encrypt_card_number, process_transaction
from backend.routers.admin import read_all_transactions
from backend.routers.admin import check_admin_user_auth
# import json

router = APIRouter()


def get_db():
    """This function returns a new database session. It is used as a
    dependency in other functions. The session is closed after the
    function is finished."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


DbDependency = Annotated[Session, Depends(get_db)]

# when an API uses this, it will enforce authorization
UserDependency = Annotated[dict, (Depends(get_current_user))]


class TransactionRequest(BaseModel):
    """This class is used to create a new transaction. It contains the
    merchant_id, customer_bank_info, merchant_bank_info, card_number,
    amount, time_stamp, and payment_type."""
    merchant_id: int
    customer_bank_info: str
    merchant_bank_info: str
    card_number: str
    amount: float
    time_stamp: datetime
    payment_type: str


class UpdateRequest(BaseModel):
    """This class is used to update a transaction. It contains the
    status of the transaction."""
    status: str


@router.post("/", status_code=status.HTTP_201_CREATED, tags=["Transaction Handling"])
async def create_transaction(user: UserDependency,
                             db: DbDependency,
                             request: TransactionRequest):
    """This function creates a new transaction. It returns a 201 status
    code if the transaction is created successfully. If the transaction
    is not created, it raises an exception. If the user is not authorized
    to create the transaction, it raises an exception."""
    check_user_authentication(user)

    try:
        encrypted_card_number = encrypt_card_number(request.card_number)
        create_transaction_model = Transactions(
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
        transaction_status = process_transaction(request.payment_type,
                                                 request.card_number,
                                                 request.amount)
        create_transaction_model.status = transaction_status
        db.commit()
        return {"message": "Transaction created successfully"}
    except Exception as e:
        message = str(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Failed to create transaction. Error Info: '
                            + message) from e


# regular user-get by user_id
@router.get("/transactions/get", tags=["Transaction Handling"])
async def get_all_transactions(user: UserDependency, db: DbDependency):
    '''
    Return all transactions relevant to this user,
    no matter the user served as customer or merchant in transactions.
    '''
    check_user_authentication(user)
    if user.get('role') == 'admin':
        return read_all_transactions(user, db)
    transactions = \
        db.query(Transactions).filter(
            Transactions.customer_id == user.get('id')
        ).all() + \
        db.query(Transactions).filter(
            Transactions.merchant_id == user.get('id')
        ).all()
    return transactions


@router.get("/transaction/{transaction_id}", status_code=status.HTTP_200_OK, tags=["Transaction Handling"])
async def get_transaction_by_id(user: UserDependency,
                                db: DbDependency,
                                transaction_id: int = Path(gt=-1)):
    """This function returns a transaction by transaction_id and give exceptions."""
    check_user_authentication(user)

    filtered_transactions = db.query(Transactions).filter(
        Transactions.transaction_id == transaction_id
    )

    transaction_model = []

    if user.get('role') == 'admin':
        transaction_model = filtered_transactions.first()
    transaction_model = \
        filtered_transactions.filter(
            Transactions.customer_id == user.get('id')
        ).all() +\
        filtered_transactions.filter(
            Transactions.merchant_id == user.get('id')
        ).all()

    if len(transaction_model) > 0:
        return transaction_model[0]
    raise HTTPException(status_code=404, detail='Transaction not found')


@router.get("/transactions/{date}", status_code=status.HTTP_200_OK, tags=["Transaction Handling"])
async def get_transactions_by_date(user: UserDependency,
                                   db: DbDependency,
                                   date: str = Path(
                                    ..., description="Date in ISO format"
                                   )):
    """This function returns all transactions for a given date and give exceptions."""
    try:
        parsed_date = datetime.strptime(date, "%Y-%m-%d")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Invalid date format or date value. \
                                    Error Info: ' + str(e)) from e

    check_user_authentication(user)
    filtered_transactions = []
    if user.get('user_role') == 'admin':
        filtered_transactions = db.query(Transactions)
    else:
        filtered_transactions = db.query(Transactions).filter(
            or_(
                Transactions.customer_id == user.get('id'),
                Transactions.merchant_id == user.get('id')
            )
        )
    transaction_model = (
        filtered_transactions
        .filter(
            extract('year', Transactions.time_stamp) == parsed_date.year
        )
        .filter(
            extract('month', Transactions.time_stamp) == parsed_date.month
        )
        .filter(
            extract('day', Transactions.time_stamp) == parsed_date.day
        ).all()
    )
    if len(transaction_model) > 0:
        return transaction_model
    raise HTTPException(status_code=404,
                        detail=f'Transaction not found on the date: {date}')


@router.get("/transactions/{start_date}/{end_date}",
            status_code=status.HTTP_200_OK,
            tags=["Transaction Handling"])
async def get_transactions_by_period(user: UserDependency,
                                     db: DbDependency,
                                     start_date: str =
                                     Path(
                                        ...,
                                        description="Start Date in ISO format"
                                     ),
                                     end_date: str =
                                     Path(
                                        ...,
                                        description="End Date in ISO format"
                                     )):
    """This function returns all transactions for a given period."""
    try:
        parsed_start_date = datetime.strptime(start_date, "%Y-%m-%d")
        # or user timedelta(days=1)
        parsed_end_date = datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Invalid date format or date value. \
                                    Error Info: ' + str(e)) from e

    check_user_authentication(user)
    filtered_transactions = []
    if user.get('user_role') == 'admin':
        filtered_transactions = db.query(Transactions)
    else:
        filtered_transactions = db.query(Transactions).filter(
            or_(
                Transactions.customer_id == user.get('id'),
                Transactions.merchant_id == user.get('id')
            )
        )
    transaction_model = (
        filtered_transactions
        .filter(
            extract('year', Transactions.time_stamp) >= parsed_start_date.year
        )
        .filter(
            extract('month', Transactions.time_stamp)
            >= parsed_start_date.month
        )
        .filter(
            extract('day', Transactions.time_stamp) >= parsed_start_date.day
        )
        .filter(
            extract('year', Transactions.time_stamp) <= parsed_end_date.year
        )
        .filter(
            extract('month', Transactions.time_stamp) <= parsed_end_date.month
        )
        .filter(
            extract('day', Transactions.time_stamp) <= parsed_end_date.day
        ).all()
    )
    if len(transaction_model) > 0:
        return transaction_model
    raise HTTPException(status_code=404,
                        detail=f'Transaction not found from \
                                {start_date} to {end_date}')


@router.get("/balance", status_code=status.HTTP_200_OK, tags=["Balance Display"])
async def get_balance_sum(user: UserDependency, db: DbDependency):
    """This function returns the sum of all transaction amounts. If the
    user is not authenticated, it raises an exception. If the user is not
    authorized to view the transaction, it raises an exception. If the
    transaction is not found, it raises an exception. If the date format
    is invalid, it raises an exception. If the date value is invalid, it
    raises an exception. If the date range is invalid, it raises an
    exception."""
    check_user_authentication(user)
    if (user.get('user_role') == 'admin'):
        filtered_transactions = db.query(Transactions)
    else:
        filtered_transactions = db.query(Transactions).filter(
            or_(
                Transactions.customer_id == user.get('id'),
                Transactions.merchant_id == user.get('id')
            )
        )
    transaction_model = (
        filtered_transactions.filter(
                            func.lower(Transactions.status) == "completed"
                        ).all()
    )

    balance = sum(transaction.amount for transaction in transaction_model)
    return balance


@router.get("/balance/{date}", status_code=status.HTTP_200_OK,tags=["Balance Display"])
async def get_balance_sum_by_date(user: UserDependency,
                                  db: DbDependency,
                                  date: str =
                                  Path(..., description="Date in ISO format")):
    """This function returns the sum of all transaction amounts for a
    given date."""
    try:
        parsed_date = datetime.strptime(date, "%Y-%m-%d")
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Invalid date format or date value. \
                                    Error Info: ' + str(exc)) from exc

    check_user_authentication(user)

    filtered_transactions = []
    if (user.get('user_role') == 'admin'):
        filtered_transactions = db.query(Transactions)
    else:
        filtered_transactions = db.query(Transactions).filter(
            or_(
                Transactions.customer_id == user.get('id'),
                Transactions.merchant_id == user.get('id')
            )
        )
    transaction_model = (
        filtered_transactions
        .filter(extract('year', Transactions.time_stamp) == parsed_date.year)
        .filter(extract('month', Transactions.time_stamp) == parsed_date.month)
        .filter(extract('day', Transactions.time_stamp) == parsed_date.day)
        .filter(func.lower(Transactions.status) == "completed").all()
    )

    balance = sum(transaction.amount for transaction in transaction_model)
    return balance


@router.get("/balance/{start_date}/{end_date}", status_code=status.HTTP_200_OK, tags=["Balance Display"])
async def get_balance_sum_by_period(user: UserDependency,
                                    db: DbDependency,
                                    start_date: str = Path(
                                        ...,
                                        description="Start Date in ISO format"
                                    ),
                                    end_date: str = Path(
                                        ...,
                                        description="End Date in ISO format"
                                    )):
    """This function returns the sum of all transaction amounts for a
    given period. If the user is not authenticated, it raises an exception.
    If the user is not authorized to view the transaction, it raises an
    exception. If the transaction is not found, it raises an exception. If
    the date format is invalid, it raises an exception. If the date value
    is invalid, it raises an exception. If the date range is invalid, it
    raises an exception."""
    try:
        parsed_start_date = datetime.strptime(start_date, "%Y-%m-%d")
        # or user timedelta(days=1)
        parsed_end_date = datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Invalid date format or date value. \
                                    Error Info: ' + str(exc)) from exc

    check_user_authentication(user)

    if (user.get('user_role') == 'admin'):
        filtered_transactions = db.query(Transactions)
    else:
        filtered_transactions = db.query(Transactions).filter(
            or_(
                Transactions.customer_id == user.get('id'),
                Transactions.merchant_id == user.get('id')
            )
        )
    transaction_model = (
        filtered_transactions
        .filter(
            extract('year', Transactions.time_stamp) >= parsed_start_date.year
        )
        .filter(
            extract('month', Transactions.time_stamp)
            >= parsed_start_date.month
        )
        .filter(
            extract('day', Transactions.time_stamp) >= parsed_start_date.day
        )
        .filter(
            extract('year', Transactions.time_stamp)
            <= parsed_end_date.year
        )
        .filter(
            extract('month', Transactions.time_stamp)
            <= parsed_end_date.month
        )
        .filter(extract('day', Transactions.time_stamp) <= parsed_end_date.day)
        .filter(func.lower(Transactions.status) == "completed").all()
    )

    if transaction_model is not None:
        balance = sum(transaction.amount for transaction in transaction_model)
        return balance
    raise HTTPException(status_code=404,
                        detail=f'Transaction not found \
                                from {start_date} to {end_date}')


# admin can update transaction by transaction_id
@router.put("/transaction/{transaction_id}",
            status_code=status.HTTP_204_NO_CONTENT, tags=["Administrative Control"])
async def update_transaction_by_id(user: UserDependency,
                                   db: DbDependency,
                                   request: UpdateRequest,
                                   transaction_id: int = Path(gt=-1)):
    """This function updates a transaction by transaction_id. It returns
    a 204 status code if the transaction is updated successfully."""
    # check_user_authentication(user)
    check_admin_user_auth(user)

    transaction_model = db.query(Transactions).filter(
        Transactions.transaction_id == transaction_id
    ).first()

    if transaction_model is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    # make the updates
    transaction_model.status = request.status
    db.commit()


# System will auto check all approved transaction
# update them when completed
# No user authentication needed
@router.put("/transactions/update", status_code=status.HTTP_204_NO_CONTENT, tags=["Transaction Status Update"])
async def auto_update_transaction(db: DbDependency):
    """This function auto updates all approved transactions to completed
    status if the transaction is older than 2 days. It returns a 204 status
    code if the transaction is updated successfully. If the transaction is
    not found, it raises an exception. If the user is not authorized to
    update the transaction, it raises an exception."""
    transaction_model = (
        db.query(Transactions).filter(Transactions.status == "approved").all()
    )

    # check_user_authentication(user)
    if transaction_model is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    # make the updates
    time_stamp = datetime.now()

    for transaction in transaction_model:
        if (
            time_stamp.year >= transaction.time_stamp.year and
            time_stamp.month >= transaction.time_stamp.month and
            (time_stamp.day >= transaction.time_stamp.day+2)
        ):
            transaction.status = "completed"
    db.commit()


# admin can delete transaction by transaction_id
@router.delete("/transaction/{transaction_id}",
               status_code=status.HTTP_204_NO_CONTENT,
               tags=["Administrative Control"])
async def delete_transaction(user: UserDependency,
                             db: DbDependency,
                             transaction_id: int = Path(gt=-1)):
    """This function deletes a transaction by transaction_id. It returns
    a 204 status code if the transaction is deleted successfully. If the
    transaction is not found, it raises an exception. If the user is not
    authorized to delete the transaction, it raises an exception."""

    check_admin_user_auth(user)

    filtered_transactions = db.query(Transactions).filter(
        Transactions.transaction_id == transaction_id
    )

    # if user.get('user_role') == "customer":
    #     filtered_transactions = filtered_transactions.filter(Transactions.customer_id
    #                             == user.get('id')).first()
    # elif user.get('user_role') == 'merchant' :
    #     filtered_transactions = filtered_transactions.filter(Transactions.merchant_id
    #                             == user.get('id')).first()
    # elif user.get('user_role') == 'admin' :
    #     filtered_transactions = filtered_transactions.first()
    # transaction_model = db.query(Transactions).filter(Transactions.transaction_id
    #                     == transaction_id).filter(Transactions.customer_id
    #                     == user.get('id')).first()

    if filtered_transactions is None:
        raise HTTPException(status_code=404, detail='Transaction not found')

    db.query(Transactions).filter(
        Transactions.transaction_id == transaction_id
    ).delete()
    db.commit()
