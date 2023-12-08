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

* The following is the '.env' file, please remeber to create it and add it to the root directory:
```
SECRET_KEY =  '4d173fb647cc7cb3dbdb802a074c26011ad134533d118effbcf8694b251a0de2'
ALGORITHM = 'HS256'
AES_KEY = 'bDgbkMg3Hvz/VA2MzKwRQ200kvhHD9gb'
- Github Issues Page: https://github.com/orgs/TrinityGo/projects/2
```

# Examples of How to Use the APP
[TODO:] how to call the API using curl or screenshots of your webpage&nbsp; 
## User Management  
### 1. Create user  
Create both regular and administrative users, specified by 'role'.  
  -  Regular user: role = "user"  
  -   Admin user: role = "admin"  

- HTTP requests using curl
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


admin
The following APIs have authorization checks in place, and only users with `admin` are allowed to access them.
1. Read all transactions

2. Read all Users
This function returns all users in the database. It is only accessible to admin users.
```
curl -X 'GET' \
  'http://ec2-54-173-190-240.compute-1.amazonaws.com:8000/admin/users' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ5IiwiaWQiOjUsInJvbGUiOiJhZG1pbiIsImV4cCI6MTcwMTk5OTQwMX0._cZ5LKdkNnxm9uzs0BzbA_m8_9LkHyhxcOgT2VygS98'
```
Response:

