from models.models import Transactions
from routers.helpers import process_transaction, validate_card, process_card
from datetime import datetime


# good_transaction_credit_card: valid number + sufficient fund
good_transaction_credit_card = Transactions(
    transaction_id = 55,
    customer_id = 1,
    merchant_id = 2,
    encrypted_info = "4147202464191053",
    amount = 100,
    time_stamp = datetime.now(),
    status = "pending",
    payment_type = "credit_card"
)

# good_transaction_debit_card: valid number + sufficient fund
good_transaction_debit_card = Transactions(
    transaction_id = 55,
    customer_id = 1,
    merchant_id = 2,
    encrypted_info = "4147202464191053",
    amount = 100,
    time_stamp = datetime.now(),
    status = "pending",
    payment_type = "debit_card"
)

# good_transaction_bank_account: valid number + sufficient fund
good_transaction_bank_account = Transactions(
    transaction_id = 55,
    customer_id = 1,
    merchant_id = 2,
    encrypted_info = "4147202464191053",
    amount = 100,
    time_stamp = datetime.now(),
    status = "pending",
    payment_type = "bank_account"
)

# bad_number_transaction_credit_card: invalid number
bad_number_transaction_credit_card = Transactions(
    transaction_id = 55,
    customer_id = 1,
    merchant_id = 2,
    encrypted_info = "0",
    amount = 100,
    time_stamp = datetime.now(),
    status = "pending",
    payment_type = "credit_card"
)

# bad_fund_transaction_credit_card: valid number + insufficient fund
bad_fund_transaction_credit_card = Transactions(
    transaction_id = 55,
    customer_id = 1,
    merchant_id = 2,
    encrypted_info = "4147202464191053",
    amount = 10000.1,
    time_stamp = datetime.now(),
    status = "pending",
    payment_type = "credit_card"
)

# bad_number_transaction_debit_card: invalid number
bad_number_transaction_debit_card = Transactions(
    transaction_id = 55,
    customer_id = 1,
    merchant_id = 2,
    encrypted_info = "0",
    amount = 100,
    time_stamp = datetime.now(),
    status = "pending",
    payment_type = "debit_card"
)

# bad_fund_transaction_debit_card: valid number + insufficient fund
bad_fund_transaction_debit_card = Transactions(
    transaction_id = 55,
    customer_id = 1,
    merchant_id = 2,
    encrypted_info = "4147202464191053",
    amount = 1000000.1,
    time_stamp = datetime.now(),
    status = "pending",
    payment_type = "debit_card"
)


def test_process_transaction():
    # assert process_transaction(good_transaction_credit_card) == 'approved'
    # assert process_transaction(good_transaction_debit_card) == 'approved'
    # assert process_transaction(bad_number_transaction_credit_card) == 'rejected'
    
    assert process_transaction(bad_fund_transaction_credit_card) == 'rejected'
    assert process_transaction(bad_number_transaction_debit_card) == 'rejected'
    assert process_transaction(bad_fund_transaction_debit_card) == 'rejected'
    assert process_transaction(good_transaction_bank_account) == 'completed'


def test_validate_card():
    assert validate_card(good_transaction_credit_card.encrypted_info) == True
    assert validate_card(good_transaction_debit_card.encrypted_info) == True
    assert validate_card(good_transaction_bank_account.encrypted_info) == True

    assert validate_card(bad_number_transaction_credit_card.encrypted_info) == False
    assert validate_card(bad_fund_transaction_credit_card.encrypted_info) == True
    assert validate_card(bad_number_transaction_debit_card.encrypted_info) == False
    assert validate_card(bad_fund_transaction_debit_card.encrypted_info) == True


def test_process_card():
    assert process_card(good_transaction_credit_card.encrypted_info, good_transaction_credit_card.amount) == True
    assert process_card(good_transaction_debit_card.encrypted_info, good_transaction_debit_card.amount) == True
    assert process_card(good_transaction_bank_account.encrypted_info, good_transaction_bank_account.amount) == True
    
    assert process_card(bad_number_transaction_credit_card.encrypted_info, bad_number_transaction_credit_card.amount) == False
    assert process_card(bad_fund_transaction_credit_card.encrypted_info, bad_fund_transaction_credit_card.amount) == False
    
    assert process_card(bad_number_transaction_debit_card.encrypted_info, bad_number_transaction_debit_card.amount) == False
    assert process_card(bad_fund_transaction_debit_card.encrypted_info, bad_fund_transaction_debit_card.amount) == False