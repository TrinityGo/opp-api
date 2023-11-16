from starlette.exceptions import HTTPException
# from Crypto.Cipher import AES
import os
from dotenv import load_dotenv
import base64
import json
import requests


load_dotenv()  # take environment variables from .env.
AES_KEY = os.environ.get("AES_KEY")
delimiter = '||'

def check_user_authentication(user):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')


def encrypt_card_info(card_number):
    # combined_data = customer_bank_info + delimiter + merchant_bank_info
    # cipher = AES.new(AES_KEY, AES.MODE_EAX)
    # cipher_text, tag = cipher.encrypt_and_digest(combined_data.encode())
    # nonce = cipher.nonce
    
    # # Convert to Base64 to ensure safe string representation
    # encoded_nonce = base64.b64encode(nonce).decode('utf-8')
    # encoded_tag = base64.b64encode(tag).decode('utf-8')
    # encoded_cipher_text = base64.b64encode(cipher_text).decode('utf-8')

    # # Create a JSON object
    # encrypted_object = json.dumps({
    #     "nonce": encoded_nonce,
    #     "tag": encoded_tag,
    #     "cipher_text": encoded_cipher_text
    # })
    # encrypted_object = json.dumps({
    #     "customer_bank_info": customer_bank_info,
    #     "merchant_bank_info": merchant_bank_info,
    # })

# encrypted_object is a JSON string that can be passed around
    return ""


# return "approved" for credit cards, "completed" for bank accounts"; return "rejected" for failure
def process_transaction(payment_type, card_number, amount):
    if(validate_card(card_number) & process_card(card_number, amount)):
        if(payment_type == "debit_card"):
            return 'completed'
        else:
            return 'approved'
    return 'rejected'


def validate_card(card_number):
    url = "https://c3jkkrjnzlvl5lxof74vldwug40pxsqo.lambda-url.us-west-2.on.aws"
    headers = {"Content-Type": "application/json"}
    data = {"card_number": card_number}
    
    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)
        result = response.json()
        return True
    except requests.exceptions.RequestException as e:
        # Handle any exceptions that may occur during the request
        print(f"Error: {e}")
        return False
        # {"success": False, "msg": "Error during API request"}


def process_card(card_number, amt):
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