from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from base64 import b64encode, b64decode
from dotenv import load_dotenv
import os

def encrypt_card_number(card_number, key):
    # Ensure the card number and key are bytes
    card_number_bytes = card_number.encode("utf-8")
    key_bytes = key.encode("utf-8")

    # Generate a random IV (Initialization Vector)
    iv = os.urandom(16)

    # Create an AES cipher with CBC mode
    cipher = Cipher(algorithms.AES(key_bytes), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # Encrypt the card number
    ciphertext = encryptor.update(card_number_bytes) + encryptor.finalize()

    # Return the IV and the encrypted card number as base64-encoded strings
    return b64encode(iv).decode("utf-8"), b64encode(ciphertext).decode("utf-8")

def decrypt_card_number(encrypted_data, key):
    # Ensure the key is bytes
    key_bytes = key.encode("utf-8")

    # Decode the IV and encrypted data from base64
    iv = b64decode(encrypted_data[0])
    ciphertext = b64decode(encrypted_data[1])

    # Create an AES cipher with CBC mode
    cipher = Cipher(algorithms.AES(key_bytes), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    # Decrypt the card number
    decrypted_data = decryptor.update(ciphertext) + decryptor.finalize()

    # Return the decrypted card number as a string
    return decrypted_data.decode("utf-8")

# Example Usage:
card_number = "1234567812345678"
load_dotenv()
encryption_key = os.environ.get("AES_KEY")

# Encrypt the card number
encrypted_data = encrypt_card_number(card_number, encryption_key)
print("Encrypted Data:", encrypted_data)

# Decrypt the card number
decrypted_card_number = decrypt_card_number(encrypted_data, encryption_key)
print("Decrypted Card Number:", decrypted_card_number)
