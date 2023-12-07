from backend.models.models import Transactions
from backend.routers.helpers import encrypt_card_number, decrypt_card_number,process_transaction, validate_card, process_card
from datetime import datetime
import random


credit_card = "credit_card"
debit_card = "debit_card"
good_card_number = "4147202464191053"
bad_card_number = "1234"
good_amount = 100
bad_amount = 10000.1


def test_process_transaction():
    assert process_transaction(credit_card, good_card_number, good_amount) == 'approved'
    assert process_transaction(credit_card, good_card_number, bad_amount) == 'rejected'
    assert process_transaction(credit_card, bad_card_number, good_amount) == 'rejected'
    assert process_transaction(credit_card, bad_card_number, bad_amount) == 'rejected'


def test_process_transaction():
    assert process_transaction(debit_card, good_card_number, good_amount) == 'completed'
    assert process_transaction(debit_card, good_card_number, bad_amount) == 'rejected'
    assert process_transaction(debit_card, bad_card_number, good_amount) == 'rejected'
    assert process_transaction(debit_card, bad_card_number, bad_amount) == 'rejected'


def test_validate_card():
    assert validate_card(good_card_number) == True
    assert validate_card(bad_card_number) == True


def test_process_card():
    assert process_card(good_card_number, good_amount) == True
    assert process_card(good_card_number, bad_amount) == False
    assert process_card(bad_card_number, good_amount) == False
    assert process_card(bad_card_number, bad_amount) == False


def test_encrypt_card_number():
    card_number = "1234567812345678"
    encrypted_data = encrypt_card_number(card_number)
    decrypted_card_number = decrypt_card_number(encrypted_data)
    assert card_number == decrypted_card_number

    card_number = str(random.randrange(0, 65536))
    encrypted_data = encrypt_card_number(card_number)
    decrypted_card_number = decrypt_card_number(encrypted_data)
    assert card_number == decrypted_card_number