# ReST API Design
- **Title:** ReST API Design
- **Date:** Nov 2, 2023
- **Author:** Yiwen Wang
- **Version:** 1.0

**Revision History**
|Date|Version|Description|Author|
|:----:|:----:|:----:|:----:|
|Nov 2, 2023|1.0|Initial release| Yiwen Wang|
-------------


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

### Successful Response
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

### Other Responses
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




