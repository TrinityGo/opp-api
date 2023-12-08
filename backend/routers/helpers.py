"""This module contains helper functions for the API routers."""
# Standard imports
import os
from base64 import b64encode, b64decode
# import base64
# import json
from starlette.exceptions import HTTPException
# Third-party imports
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()  # take environment variables from .env.
# These are used to create the signature for a JWT
AES_KEY = os.environ.get("AES_KEY")
if AES_KEY is None:
    AES_KEY = os.getenv("AES_KEY")


def check_user_authentication(user):
    """This function checks if the user is authenticated.
    If not, it raises an exception."""
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')


def encrypt_card_number(card_number):
    """This function encrypts a card number using AES encryption
    with a provided key."""
    # Ensure the card number and key are bytes
    card_number_bytes = card_number.encode("utf-8")
    key_bytes = AES_KEY.encode("utf-8")

    # Generate a random IV (Initialization Vector)
    iv = os.urandom(16)

    # Create an AES cipher with CBC mode
    cipher = Cipher(algorithms.AES(key_bytes),
                    modes.CFB(iv),
                    backend=default_backend())
    encryptor = cipher.encryptor()

    # Encrypt the card number
    ciphertext = encryptor.update(card_number_bytes) + encryptor.finalize()

    # Return the IV and the encrypted card number as base64-encoded strings
    return {"iv": b64encode(iv).decode("utf-8"),
            "crypted_text": b64encode(ciphertext).decode("utf-8")}


def decrypt_card_number(encrypted_data):
    """This function decrypts a card number using AES decryption with a provided key."""
    # Ensure the key is bytes
    key_bytes = AES_KEY.encode("utf-8")

    # Decode the IV and encrypted data from base64
    iv = b64decode(encrypted_data["iv"])
    ciphertext = b64decode(encrypted_data["crypted_text"])

    # Create an AES cipher with CBC mode
    cipher = Cipher(algorithms.AES(key_bytes),
                    modes.CFB(iv),
                    backend=default_backend())
    decryptor = cipher.decryptor()

    # Decrypt the card number
    decrypted_data = decryptor.update(ciphertext) + decryptor.finalize()

    # Return the decrypted card number as a string
    return decrypted_data.decode("utf-8")


# return "approved" for credit cards, "completed" for bank accounts";
# return "rejected" for failure
def process_transaction(payment_type, card_number, amount):
    """This function processes a transaction. It returns 'approved' for
    credit cards, 'completed' for bank accounts, and 'rejected' for failure."""
    if validate_card(card_number) & process_card(card_number, amount):
        if payment_type == "debit_card":
            return 'completed'
        return 'approved'
    return 'rejected'


def validate_card(card_number):
    """This function validates a card number.
    It returns True if the card number is valid, and False otherwise."""
    url = "https://c3jkkrjnzlvl5lxof74vldwug40pxsqo.lambda-url.us-west-2.on.aws"
    headers = {"Content-Type": "application/json"}
    data = {"card_number": card_number}

    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)
        # result = response.json()
        return True
    except requests.exceptions.RequestException as e:
        # Handle any exceptions that may occur during the request
        print(f"Error: {e}")
        return False
        # {"success": False, "msg": "Error during API request"}


def process_card(card_number, amt):
    """This function processes a card transaction.
    It returns True if the transaction is successful, and False otherwise."""
    url = "https://223didiouo3hh4krxhm4n4gv7y0pfzxk.lambda-url.us-west-2.on.aws"
    headers = {"Conetent-Type": "application/json"}
    data = {"card_number": f"{card_number}", "amt": f"{amt}"}

    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        # {'msg': 'Insufficient funds and/or fraudulent card', 'success': 'false'}
        result = response.json()
        return result['success'] == 'true'
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return False
