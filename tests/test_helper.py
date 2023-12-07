"""Test the helper functions"""

# Standard imports
import random
from backend.routers.helpers import encrypt_card_number, decrypt_card_number
from backend.routers.helpers import process_transaction, validate_card, process_card


CREDIT_CARD = "credit_card"
DEBIT_CARD = "debit_card"
GOOD_CARD_NUMBER = "4147202464191053"
BAD_CARD_NUMBER = "1234"
GOOD_AMOUNT = 100
BAD_AMOUNT = 10000.1


def test_process_transaction():
    """Test the process_transaction function."""
    assert process_transaction(CREDIT_CARD, GOOD_CARD_NUMBER, GOOD_AMOUNT) == 'approved'
    assert process_transaction(CREDIT_CARD, GOOD_CARD_NUMBER, BAD_AMOUNT) == 'rejected'
    assert process_transaction(CREDIT_CARD, BAD_CARD_NUMBER, GOOD_AMOUNT) == 'rejected'
    assert process_transaction(CREDIT_CARD, BAD_CARD_NUMBER, BAD_AMOUNT) == 'rejected'

def test_validate_card():
    """Test the validate_card function."""
    assert validate_card(GOOD_CARD_NUMBER) is True
    assert validate_card(BAD_CARD_NUMBER) is True


def test_process_card():
    """Test the process_card function."""
    assert process_card(GOOD_CARD_NUMBER, GOOD_AMOUNT) is True
    assert process_card(GOOD_CARD_NUMBER, BAD_AMOUNT) is False
    assert process_card(BAD_CARD_NUMBER, GOOD_AMOUNT) is False
    assert process_card(BAD_CARD_NUMBER, BAD_AMOUNT) is False


def test_encrypt_card_number():
    """Test the encrypt_card_number function."""
    card_number = "1234567812345678"
    encrypted_data = encrypt_card_number(card_number)
    decrypted_card_number = decrypt_card_number(encrypted_data)
    assert card_number == decrypted_card_number

    card_number = str(random.randrange(0, 65536))
    encrypted_data = encrypt_card_number(card_number)
    decrypted_card_number = decrypt_card_number(encrypted_data)
    assert card_number == decrypted_card_number
