# Endpoint Documentation
- **Title:** Endpoint Documentation
- **Course:** NEU CS5500 Fall 2023
- **Date:** Dec 7, 2023
- **Author:** Yiwen Wang, Xinyi Gao, Yijia Ma
- **Version:** 2.0
- **Contents:** Detail the required request parameters, acceptable request methods (GET, POST, PUT, DELETE), and expected response formats

**Revision History**
|Date|Version|Description|Author|
|:----:|:----:|:----:|:----:|
|Nov 9, 2023|1.0|Initial release| Yiwen Wang|
|Dec 7, 2023|2.0|Update API| Yiwen Wang|

## Overview
This document lists all the API endpoints along with their descriptions, request parameters, and response formats.

### Admin Endpoints
- **GET /admin/transactions**: Retrieve all transactions. Restricted to admin users.
- **GET /admin/users**: Retrieve all users. Restricted to admin users.

### Authentication Endpoints
- **POST /auth/**: Create a new user.
- **POST /auth/token/**: Authenticate and receive an access token.

### Transaction Endpoints
- **POST /transactions/**: Create a new transaction.
- **GET /transactions/get**: Retrieve all transactions for the authenticated user.

### Models
- `Users`: Represents user data with attributes like email, username, role, etc.
- `Transactions`: Represents transaction data with fields like transaction_id, customer_id, amount, etc.

### Example Request and Response
**POST /transactions/**
```json
Request:
{
  "merchant_id": 0,
  "customer_bank_info": "string",
  "merchant_bank_info": "string",
  "card_number": "string",
  "amount": 0,
  "time_stamp": "2023-12-07T19:19:58.984Z",
  "payment_type": "string"
}
```

**Response:**
```json
{
  "message": "Transaction created successfully"
}
```

### Database Configuration
* database.py configures the SQLAlchemy engine and session.
* SQLALCHEMY_DATABASE_URL determines the database connection, supporting SQLite and PostgreSQL.

### Alembic Integration
* env.py configures Alembic for database migrations, including offline and online migration support.