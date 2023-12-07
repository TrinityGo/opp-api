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
- Github Issues Page: https://github.com/TrinityGo/opp-api/issues
```

# Examples of How to Use the APP
[TODO:] how to call the API using curl or screenshots of your webpage
