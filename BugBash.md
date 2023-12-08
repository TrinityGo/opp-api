# BugBash - TrinityGo Online-payment Processing Platform (OPP)
- **Title:** Project BugBash File
- **Course:** NEU CS5500 Fall 2023
- **Date:** Dec 7, 2023
- **Author:** Yiwen Wang, Xinyi Gao, Yijia Ma

# Introduction
- This is a bugbash file to our project. 
- Our App's URL：
## Instructions for use
### Initial Installation
* Create a virtual environment
  * `pip install virtualenv`
  * `virtualenv env`
* Activate the virtual environment
  * on macOS and Linux, use:
    * `source env/bin/activate`
  * on Windows, use:
    * `env\Scripts\activate`
* Install the required' dependencies
  * `pip install -r requirements.txt`
* Open a terminal to the root of the repository and run the following command:
  * `uvicorn backend.main:app --reload`
* Upload `.env` file to root directory

### Post-Installation & Swagger UI
* Open the following URL on a browser of your choice: `http://127.0.0.1:8000/docs`
* Since all the API's are protected, you need to authenticate and authorize yourself
  * create user via `/auth` endpoint
  * authenticate and authorize user via `authorize` button at top right corner
* Tests are working in this environment as well

```
- Github Issues Page: https://github.com/orgs/TrinityGo/projects/2
```

# Examples of How to Use the APP
[TODO:] how to call the API using curl or screenshots of your webpage&nbsp; 
## User Management  
### 1. Create User  
Create both regular and administrative users, specified by 'role'.  
  -  Regular user: role = "customer/merchant"  
  -   Admin user: role = "admin"  

- HTTP requests using curl
Request URL: http://ec2-54-173-190-240.compute-1.amazonaws.com:8000/auth/
```
curl -X 'POST' \
  'http://ec2-54-173-190-240.compute-1.amazonaws.com:8000/auth/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "email": "Yijia@gmail.com",
  "username": "y",
  "first_name": "Yijia",
  "surname": "Ma",
  "password": "123",
  "role": "admin"
}'
```
- Triggered Action  
Add the following created user to the database.  
Return a successful response with status_code 201.
```
{
    "email": "Yijia@gmail.com",
    "id": 2,
    "first_name": "Yijia",
    "hashed_password": "$2b$12$FEDXBwxzZdPZbjbb/XPkLeOSKu00a1H7XQe8cDMW2m1JRzAL51HPC",
    "role": "admin",
    "username": "y",
    "surname": "Ma",
    "is_active": true,
    "phone_number": null
  }
```
- Response body
```
{
  "message": "User created successfully"
}
```

### 2. Login For Access Token
This function logs in a user and generates an access token. 

- HTTP requests using curl  
Request URL: http://ec2-54-173-190-240.compute-1.amazonaws.com:8000/auth/token/
```
curl -X 'POST' \
  'http://ec2-54-173-190-240.compute-1.amazonaws.com:8000/auth/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "email": "Yijia@gmail.com",
  "username": "y",
  "first_name": "Yijia",
  "surname": "Ma",
  "password": "123",
  "role": "admin"
}'
```
- Triggered Action  
User successfully logs in.  
Return a successful response with status_code 200.

- Response body
```
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ5IiwiaWQiOjUsInJvbGUiOiJhZG1pbiIsImV4cCI6MTcwMjAwMDQyNX0.AzG9_atGNytsrYTu1TV8kekjUrG3rOLu2XB9xyzjHzo",
  "token_type": "bearer"
}
```
### 3. Get Current User  
This function retrieves information about the current user from the provided token.

- HTTP requests using curl  
Request URL: http://ec2-54-173-190-240.compute-1.amazonaws.com:8000/auth/user
```
curl -X 'POST' \
  'http://ec2-54-173-190-240.compute-1.amazonaws.com:8000/auth/user' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ5IiwiaWQiOjUsInJvbGUiOiJhZG1pbiIsImV4cCI6MTcwMTk5OTQwMX0._cZ5LKdkNnxm9uzs0BzbA_m8_9LkHyhxcOgT2VygS98' \
  -d ''
```  
- Triggered Action  
Return a successful response with status_code 201.
- Response body
```
{
  "username": "y",
  "id": 5,
  "user_role": "admin"
}
```
## Administrative Control  
The following APIs have authorization checks in place, and only users with `admin` are allowed to access them.
### 1. Read All Transactions  
This function returns all transactions in the database. It is only accessible to admin users.
- HTTP requests using curl  
Request URL: http://ec2-54-173-190-240.compute-1.amazonaws.com:8000/admin/transactions
```
curl -X 'GET' \
  'http://ec2-54-173-190-240.compute-1.amazonaws.com:8000/admin/transactions' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ5IiwiaWQiOjUsInJvbGUiOiJhZG1pbiIsImV4cCI6MTcwMTk5OTQwMX0._cZ5LKdkNnxm9uzs0BzbA_m8_9LkHyhxcOgT2VygS98'
```  
- Triggered Action  
Return a successful response with status_code 200.
- Response body
```
[
  {
    "merchant_bank_info": "Amex",
    "customer_id": 3,
    "merchant_id": 0,
    "amount": 20,
    "status": "completed",
    "transaction_id": 1,
    "customer_bank_info": "Discovery",
    "encrypted_card_number": {
      "iv": "1n+rQE6+7EtzYmgdjWI6tg==",
      "crypted_text": "sHI/7F3iiYH0qEmFRSzP"
    },
    "time_stamp": "2023-12-08T00:37:42.430000",
    "payment_type": "debit_card"
  },
  {
    "merchant_bank_info": "Discovery",
    "customer_id": 3,
    "merchant_id": 1,
    "amount": 10,
    "status": "completed",
    "transaction_id": 2,
    "customer_bank_info": "Amex",
    "encrypted_card_number": {
      "iv": "iWWbPDn3XOQb4vNwAo9T9Q==",
      "crypted_text": "SUvyerwsK/arw+NEQmgk"
    },
    "time_stamp": "2023-12-08T00:37:42.430000",
    "payment_type": "debit_card"
  },
  {
    "merchant_bank_info": "Discovery",
    "customer_id": 3,
    "merchant_id": 4,
    "amount": 30,
    "status": "completed",
    "transaction_id": 3,
    "customer_bank_info": "Amex",
    "encrypted_card_number": {
      "iv": "dFQ/D3Ka91uFs5TIYMpGAg==",
      "crypted_text": "n+pJWidUSAPpi2KukZFY"
    },
    "time_stamp": "2023-12-08T00:37:42.430000",
    "payment_type": "debit_card"
  },
  {
    "merchant_bank_info": "Amex",
    "customer_id": 3,
    "merchant_id": 1,
    "amount": 100,
    "status": "approved",
    "transaction_id": 4,
    "customer_bank_info": "Discovery",
    "encrypted_card_number": {
      "iv": "utqelXy/UO6Vt1AVVBVEjw==",
      "crypted_text": "I+QFgAC6LhFv96ZWb3CM"
    },
    "time_stamp": "2023-12-08T01:24:23.525000",
    "payment_type": "credit_card"
  }
]
```
### 2. Read all Users  
This function returns all users in the database. It is only accessible to admin users.  
- HTTP requests using curl  
Request URL: http://ec2-54-173-190-240.compute-1.amazonaws.com:8000/admin/users
```
curl -X 'GET' \
  'http://ec2-54-173-190-240.compute-1.amazonaws.com:8000/admin/users' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ5IiwiaWQiOjUsInJvbGUiOiJhZG1pbiIsImV4cCI6MTcwMTk5OTQwMX0._cZ5LKdkNnxm9uzs0BzbA_m8_9LkHyhxcOgT2VygS98'
```  
- Triggered Action  
Return a successful response with status_code 200.
- Response body
```
[
  {
    "username": "newuser",
    "surname": "User",
    "first_name": "New",
    "is_active": true,
    "phone_number": null,
    "email": "newuser@example.com",
    "id": 1,
    "hashed_password": "$2b$12$p4b.1pMDF86wVvpU7BrScOeFpQhFaMfqrd21s.6htwzftAysFTQlG",
    "role": "customer"
  },
  {
    "username": "sharon_admin",
    "surname": "gao",
    "first_name": "sharon",
    "is_active": true,
    "phone_number": null,
    "email": "sharongao_admin@gmail.com",
    "id": 4,
    "hashed_password": "$2b$12$CoTUVLuJ3p4bCNlnzSE8kuvOY9pP3XckC0izSYr66WTSQhjgF7MK2",
    "role": "admin"
  },
  {
    "username": "y",
    "surname": "Ma",
    "first_name": "Yijia",
    "is_active": true,
    "phone_number": null,
    "email": "Yijia@gmail.com",
    "id": 5,
    "hashed_password": "$2b$12$C9z4oM1uF9/bXwLckf7jtuqK1gd1PI3of3voTxA12vJN1XJOEozGm",
    "role": "admin"
  }
]
```
### 3. Update Transaction By ID  
This function updates a transaction by transaction_id. It returns a 204 status code if the transaction is updated successfully.  
- HTTP requests using curl  
Request URL: http://ec2-54-173-190-240.compute-1.amazonaws.com:8000/transaction/1
```
curl -X 'PUT' \
  'http://ec2-54-173-190-240.compute-1.amazonaws.com:8000/transaction/1' \
  -H 'accept: */*' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ5IiwiaWQiOjUsInJvbGUiOiJhZG1pbiIsImV4cCI6MTcwMjAwMTI1M30.ifqYei7tNiV72IeinlNm-j_F7XCdzIKRikmaU7lk00g' \
  -H 'Content-Type: application/json' \
  -d '{
  "status": "pending"
}'
```
- Triggered Action  
Return a successful response with status_code 204.

### 4. Login For Access Token
- HTTP requests using curl  
Request URL: http://ec2-54-173-190-240.compute-1.amazonaws.com:8000/transaction/4
```
curl -X 'DELETE' \
  'http://ec2-54-173-190-240.compute-1.amazonaws.com:8000/transaction/4' \
  -H 'accept: */*' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ5IiwiaWQiOjUsInJvbGUiOiJhZG1pbiIsImV4cCI6MTcwMjAwMTI1M30.ifqYei7tNiV72IeinlNm-j_F7XCdzIKRikmaU7lk00g'
```
- Triggered Action  
Return a successful response with status_code 204.
## Transaction Handling 
### 1. Create transaction
This function creates a new transaction. 
  - It returns a 201 status code if the transaction is created successfully. 
  - If the transaction is not created, it raises an exception.- If the user is not authorized to create the transaction, it raises an exception.


- HTTP requests using curl
```
curl -X 'POST' \
  'http://ec2-54-173-190-240.compute-1.amazonaws.com:8000/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "merchant_id": 1,
  "customer_bank_info": "Discovery",
  "merchant_bank_info": "Amex",
  "card_number": "378282246310005",
  "amount": 100,
  "time_stamp": "2023-12-08T01:24:23.525Z",
  "payment_type": "credit_card"
}'
```
- Triggered Action
```
{
  "merchant_id": 1,
  "customer_bank_info": "Discovery",
  "merchant_bank_info": "Amex",
  "card_number": "378282246310005",
  "amount": 100,
  "time_stamp": "2023-12-08T01:24:23.525Z",
  "payment_type": "credit_card"
}
```
- Response Body
```
{
  "message": "Transaction created successfully"
}
```

### 2. Get all transactions
Return all transactions relevant to this user, no matter the user served as customer or merchant in transactions.


- HTTP requests using curl
```
curl -X 'GET' \
  'http://ec2-54-173-190-240.compute-1.amazonaws.com:8000/transactions/get' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzaGFyb25fdXNlciIsImlkIjozLCJyb2xlIjoidXNlciIsImV4cCI6MTcwMjAwMDUzNX0.0Z62mP0QPddvZ7buFtE_GMcnwnHUDqABzj65H5t29Yo'
```
- Response Body
```
[
  {
    "merchant_bank_info": "Amex",
    "customer_id": 3,
    "merchant_id": 0,
    "amount": 20,
    "status": "completed",
    "transaction_id": 1,
    "customer_bank_info": "Discovery",
    "encrypted_card_number": {
      "iv": "1n+rQE6+7EtzYmgdjWI6tg==",
      "crypted_text": "sHI/7F3iiYH0qEmFRSzP"
    },
    "time_stamp": "2023-12-08T00:37:42.430000",
    "payment_type": "debit_card"
  },
  {
    "merchant_bank_info": "Discovery",
    "customer_id": 3,
    "merchant_id": 1,
    "amount": 10,
    "status": "completed",
    "transaction_id": 2,
    "customer_bank_info": "Amex",
    "encrypted_card_number": {
      "iv": "iWWbPDn3XOQb4vNwAo9T9Q==",
      "crypted_text": "SUvyerwsK/arw+NEQmgk"
    },
    "time_stamp": "2023-12-08T00:37:42.430000",
    "payment_type": "debit_card"
  },
  {
    "merchant_bank_info": "Discovery",
    "customer_id": 3,
    "merchant_id": 4,
    "amount": 30,
    "status": "completed",
    "transaction_id": 3,
    "customer_bank_info": "Amex",
    "encrypted_card_number": {
      "iv": "dFQ/D3Ka91uFs5TIYMpGAg==",
      "crypted_text": "n+pJWidUSAPpi2KukZFY"
    },
    "time_stamp": "2023-12-08T00:37:42.430000",
    "payment_type": "debit_card"
  },
  {
    "merchant_bank_info": "Amex",
    "customer_id": 3,
    "merchant_id": 1,
    "amount": 100,
    "status": "approved",
    "transaction_id": 4,
    "customer_bank_info": "Discovery",
    "encrypted_card_number": {
      "iv": "utqelXy/UO6Vt1AVVBVEjw==",
      "crypted_text": "I+QFgAC6LhFv96ZWb3CM"
    },
    "time_stamp": "2023-12-08T01:24:23.525000",
    "payment_type": "credit_card"
  }
]
```

### 3. Get transactions by Id
This function returns a transaction by transaction_id and give exceptions.

- HTTP requests using curl
```
curl -X 'GET' \
  'http://ec2-54-173-190-240.compute-1.amazonaws.com:8000/transaction/1' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzaGFyb25fdXNlciIsImlkIjozLCJyb2xlIjoidXNlciIsImV4cCI6MTcwMjAwMDUzNX0.0Z62mP0QPddvZ7buFtE_GMcnwnHUDqABzj65H5t29Yo'
```

- Triggering Action
```
URL/transaction/1
```

- Response Body
```
{
  "merchant_bank_info": "Amex",
  "customer_id": 3,
  "merchant_id": 0,
  "amount": 20,
  "status": "completed",
  "transaction_id": 1,
  "customer_bank_info": "Discovery",
  "encrypted_card_number": {
    "iv": "1n+rQE6+7EtzYmgdjWI6tg==",
    "crypted_text": "sHI/7F3iiYH0qEmFRSzP"
  },
  "time_stamp": "2023-12-08T00:37:42.430000",
  "payment_type": "debit_card"
}
```

### 4. Get Transactions by Date
This function returns all transactions for a given date and give exceptions.
- HTTP request curl
```
curl -X 'GET' \
  'http://ec2-54-173-190-240.compute-1.amazonaws.com:8000/transactions/2023-12-08' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzaGFyb25fdXNlciIsImlkIjozLCJyb2xlIjoidXNlciIsImV4cCI6MTcwMjAwMDUzNX0.0Z62mP0QPddvZ7buFtE_GMcnwnHUDqABzj65H5t29Yo'
```
- Response Body
```
[
  {
    "merchant_bank_info": "Amex",
    "customer_id": 3,
    "merchant_id": 0,
    "amount": 20,
    "status": "completed",
    "transaction_id": 1,
    "customer_bank_info": "Discovery",
    "encrypted_card_number": {
      "iv": "1n+rQE6+7EtzYmgdjWI6tg==",
      "crypted_text": "sHI/7F3iiYH0qEmFRSzP"
    },
    "time_stamp": "2023-12-08T00:37:42.430000",
    "payment_type": "debit_card"
  },
  {
    "merchant_bank_info": "Discovery",
    "customer_id": 3,
    "merchant_id": 1,
    "amount": 10,
    "status": "completed",
    "transaction_id": 2,
    "customer_bank_info": "Amex",
    "encrypted_card_number": {
      "iv": "iWWbPDn3XOQb4vNwAo9T9Q==",
      "crypted_text": "SUvyerwsK/arw+NEQmgk"
    },
    "time_stamp": "2023-12-08T00:37:42.430000",
    "payment_type": "debit_card"
  },
  {
    "merchant_bank_info": "Discovery",
    "customer_id": 3,
    "merchant_id": 4,
    "amount": 30,
    "status": "completed",
    "transaction_id": 3,
    "customer_bank_info": "Amex",
    "encrypted_card_number": {
      "iv": "dFQ/D3Ka91uFs5TIYMpGAg==",
      "crypted_text": "n+pJWidUSAPpi2KukZFY"
    },
    "time_stamp": "2023-12-08T00:37:42.430000",
    "payment_type": "debit_card"
  },
  {
    "merchant_bank_info": "Amex",
    "customer_id": 3,
    "merchant_id": 1,
    "amount": 100,
    "status": "approved",
    "transaction_id": 4,
    "customer_bank_info": "Discovery",
    "encrypted_card_number": {
      "iv": "utqelXy/UO6Vt1AVVBVEjw==",
      "crypted_text": "I+QFgAC6LhFv96ZWb3CM"
    },
    "time_stamp": "2023-12-08T01:24:23.525000",
    "payment_type": "credit_card"
  }
]
```

### 5. Get Transactions by Period
This function returns all transactions for a given period.

- HTTP request by curl
```
curl -X 'GET' \
  'http://ec2-54-173-190-240.compute-1.amazonaws.com:8000/transactions/2023-12-01/2023-12-10' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzaGFyb25fdXNlciIsImlkIjozLCJyb2xlIjoidXNlciIsImV4cCI6MTcwMjAwMDUzNX0.0Z62mP0QPddvZ7buFtE_GMcnwnHUDqABzj65H5t29Yo'
```
- Triggering Action
```
URL/transactions/<start-date>/<end-date>
```
- Response body
```
[
  {
    "merchant_bank_info": "Amex",
    "customer_id": 3,
    "merchant_id": 0,
    "amount": 20,
    "status": "completed",
    "transaction_id": 1,
    "customer_bank_info": "Discovery",
    "encrypted_card_number": {
      "iv": "1n+rQE6+7EtzYmgdjWI6tg==",
      "crypted_text": "sHI/7F3iiYH0qEmFRSzP"
    },
    "time_stamp": "2023-12-08T00:37:42.430000",
    "payment_type": "debit_card"
  },
  {
    "merchant_bank_info": "Discovery",
    "customer_id": 3,
    "merchant_id": 1,
    "amount": 10,
    "status": "completed",
    "transaction_id": 2,
    "customer_bank_info": "Amex",
    "encrypted_card_number": {
      "iv": "iWWbPDn3XOQb4vNwAo9T9Q==",
      "crypted_text": "SUvyerwsK/arw+NEQmgk"
    },
    "time_stamp": "2023-12-08T00:37:42.430000",
    "payment_type": "debit_card"
  },
  {
    "merchant_bank_info": "Discovery",
    "customer_id": 3,
    "merchant_id": 4,
    "amount": 30,
    "status": "completed",
    "transaction_id": 3,
    "customer_bank_info": "Amex",
    "encrypted_card_number": {
      "iv": "dFQ/D3Ka91uFs5TIYMpGAg==",
      "crypted_text": "n+pJWidUSAPpi2KukZFY"
    },
    "time_stamp": "2023-12-08T00:37:42.430000",
    "payment_type": "debit_card"
  },
  {
    "merchant_bank_info": "Amex",
    "customer_id": 3,
    "merchant_id": 1,
    "amount": 100,
    "status": "approved",
    "transaction_id": 4,
    "customer_bank_info": "Discovery",
    "encrypted_card_number": {
      "iv": "utqelXy/UO6Vt1AVVBVEjw==",
      "crypted_text": "I+QFgAC6LhFv96ZWb3CM"
    },
    "time_stamp": "2023-12-08T01:24:23.525000",
    "payment_type": "credit_card"
  }
]
```

## Balance Display
### 1. Get Balance Sum
This function returns the sum of all transaction amounts. 
- If the user is not authenticated, it raises an exception. 
- If the user is not authorized to view the transaction, it raises an exception. 
- If the transaction is not found, it raises an exception. 
- If the date format is invalid, it raises an exception. 
- If the date value is invalid, it raises an exception. 
- If the date range is invalid, it raises an exception.

- HTTP request by curl
```
curl -X 'GET' \
  'http://ec2-54-173-190-240.compute-1.amazonaws.com:8000/balance' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzaGFyb25fdXNlciIsImlkIjozLCJyb2xlIjoidXNlciIsImV4cCI6MTcwMjAwMDUzNX0.0Z62mP0QPddvZ7buFtE_GMcnwnHUDqABzj65H5t29Yo'
```
- Triggering Action
```
URL/balance
```
- Response body
```
60
```

### 2. Get Balance Sum by Date
This function returns the sum of all transaction amounts for a given date.
- HTTP request by curl
```
curl -X 'GET' \
  'http://ec2-54-173-190-240.compute-1.amazonaws.com:8000/balance/2023-12-08' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzaGFyb25fdXNlciIsImlkIjozLCJyb2xlIjoidXNlciIsImV4cCI6MTcwMjAwMDUzNX0.0Z62mP0QPddvZ7buFtE_GMcnwnHUDqABzj65H5t29Yo'
```
- Triggering Action
```
URL/balance/2023-12-08
```
- Response body
```
60
```

### 3. Get Balance Sum by Period
This function returns the sum of all transaction amounts for a given period. 
- If the user is not authenticated, it raises an exception. 
- If the user is not authorized to view the transaction, it raises an exception. 
- If the transaction is not found, it raises an exception. 
- If the date format is invalid, it raises an exception. 
- If the date value is invalid, it raises an exception. 
- If the date range is invalid, it raises an exception.

####    

- HTTP request by curl
```
curl -X 'GET' \
  'http://ec2-54-173-190-240.compute-1.amazonaws.com:8000/balance/2023-12-01/2023-12-10' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzaGFyb25fdXNlciIsImlkIjozLCJyb2xlIjoidXNlciIsImV4cCI6MTcwMjAwMDUzNX0.0Z62mP0QPddvZ7buFtE_GMcnwnHUDqABzj65H5t29Yo'
```
- Triggering Action
```
URL/balance/<start-date>/<end-date>
```
- Response body
```
40
```

## Transaction Status Update
### 1. Auto Update Transaction
This function auto updates all approved transactions to completed status if the transaction is older than 2 days. It returns a 204 status code if the transaction is updated successfully. If the transaction is not found, it raises an exception. If the user is not authorized to update the transaction, it raises an exception.

- HTTP request by curl
```
curl -X 'PUT' \
  'http://ec2-54-173-190-240.compute-1.amazonaws.com:8000/transactions/update' \
  -H 'accept: */*'
```
- Response body
  - No response body returned. 
  - A status code is returned.