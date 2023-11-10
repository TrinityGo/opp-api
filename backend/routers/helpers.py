from starlette.exceptions import HTTPException
# from Crypto.Cipher import AES
import os
from dotenv import load_dotenv
import base64
import json




load_dotenv()  # take environment variables from .env.
AES_KEY = os.environ.get("AES_KEY")
delimiter = '||'

def check_user_authentication(user):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')



def encrypt_transaction_info(customer_bank_info, merchant_bank_info):
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
    encrypted_object = json.dumps({
        "customer_bank_info": customer_bank_info,
        "merchant_bank_info": merchant_bank_info,
    })

# encrypted_object is a JSON string that can be passed around
    return encrypted_object

def process_transaction(transaction_model):
    return 'approved'