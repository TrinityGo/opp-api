# ReST API Design
- **Title:** ReST API Design
- **Date:** Nov 2, 2023
- **Author:** Yiwen Wang
- **Version:** 1.1

**Revision History**
|Date|Version|Description|Author|
|:----:|:----:|:----:|:----:|
|Nov 2, 2023|1.0|Initial release| Yiwen Wang|
|Nov 2, 2023|1.1|Update API| Yiwen Wang|
-------------

## User Authentication
### Register User
```python
POST /api/users/register

Request Fields:
- username (String): The desired username
- email (String): The user's email address
- password (String): The user's password

Response:
- HTTP 201 Created on success with user object
- HTTP 400 Bad Request on validation error
```

### Login User
```python
POST /api/users/login

Request Fields:
- username (String): The username
- password (String): The password

Response:
- HTTP 200 OK on success with access token
- HTTP 401 Unauthorized on failure
```

## Account Management
### Get User Profile
```Python
GET /api/users/{userId}/profile

Response:
- HTTP 200 OK with user profile data
- HTTP 404 Not Found if user does not exist
```

### Update User Profile
```python
PUT /api/users/{userId}/profile

Request Fields:
- email (String): New email address
- phone (String): New phone number

Response:
- HTTP 200 OK on success
- HTTP 400 Bad Request on validation error
```

## Payment Processing
### Initiate Payment
```python
POST /api/payments/initiate

Request Fields:
- amount (Decimal): The amount to be paid
- currency (String): The currency code (e.g., USD, EUR)
- recipientId (String): The ID of the payment recipient

Response:
- HTTP 200 OK on success with payment details
- HTTP 400 Bad Request on error
```

### Complete Payment
```python
POST /api/payments/{paymentId}/complete

Request Fields:
- paymentId (String): The unique ID of the payment
- payerId (String): The ID of the user making the payment

Response:
- HTTP 200 OK on success
- HTTP 400 Bad Request on error
```

## Transaction History
### Get Transaction History
```python
GET /api/users/{userId}/transactions

Response:
- HTTP 200 OK with a list of transactions
- HTTP 404 Not Found if user does not exist
```

## Endpoint Description
Retrieve a list of items based on the title provided as a query parameter. If no title is provided, all items will be retrieved.

### API Endpoint
```
GET /api/items/{item_id}/?title=
```

### Request Fields
| Field Name  | Field Type  | Field Description    |
|:------------|:------------|:---------------------|
| item_id     | String      | The unique ID of item|


### Query Parameters
| Parameter Name | Parameter Type | Description            |
|:---------------|:---------------|:-----------------------|
| title     | String      | Title of the item to search for|

### Request Headers
| Header Name | Header Value     |
|:------------|:-----------------|
| Accept      | application/json | 

### Example Request
```sh
$ curl 'http://localhost:8000/api/items/123?title=learn%20fastapi' -i -H 'Accept: application/json'
```

## Successful Response
- **Status Code:** 200 OK
- **Content-Type:** application/json
- **Response Body:**

```json
[
  {
    "id": "123",
    "title": "learn fastapi",
    "owner_id": 1,
    "priority": 3,
    "complete": false,
    "description": "A tutorial on learning FastAPI"
  }
]
```

## Other Responses
1. **301 Moved Permanently** (if the API endpoint has been changed)
    - **Content-Type:** application/json
    - **Response Body:** (A list of new URLs or information about the change)
```json
{
  "message": "The API endpoint has been moved permanently. Please refer to the documentation for the new endpoint."
}
```

2. **400 Bad Request** (if there's an issue with the client's request)
    - **Content-Type:** application/json
    - **Response Body:**
```json
{
  "error": "Bad Request",
  "message": "The 'item_id' provided is invalid."
}
```

3. **404 Not Found** (if the item with provided item_id does not exist)
    - **Content-Type:** application/json
    - **Response Body:**
```json
{
  "error": "Not Found",
  "message": "The item with the specified ID was not found."
}
```

4. **500 Internal Server Error** (if there's a server-side issue processing the request)
    - **Content-Type:** application/json
    - **Response Body:**
```json
{
  "error": "Internal Server Error",
  "message": "The server encountered an unexpected condition that prevented it from fulfilling the request."
}
```
    


## Notes:
1. The API uses the **'GET'** method to retrieve data, which is suitable for fetching resources.
2. The **'item_id'** in the path allows for retrieving a specific item or a collection of items if a more general endpoint is hit.
3. The **'title'** query parameter is optional and is used to filter results based on the title of the items.
4. Proper error handling is demonstrated through the use of different HTTP status codes and messages in the response to inform the client about the nature of the error encountered.

This design lays out the basic structure and expectations for interacting with the endpoint, which frontend and backend developers can follow to ensure proper integration.




