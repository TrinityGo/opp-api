# Authorization Documentation
- **Title:** Authorization Documentation
- **Course:** NEU CS5500 Fall 2023
- **Date:** Dec 7, 2023
- **Author:** Yiwen Wang, Xinyi Gao, Yijia Ma
- **Version:** 2.0
- **Contents:** Explain how to obtain and use API keys or token

**Revision History**
|Date|Version|Description|Author|
|:----:|:----:|:----:|:----:|
|Nov 9, 2023|1.0|Initial release| Yiwen Wang|
|Dec 7, 2023|2.0|API update| Yiwen Wang|

## Overview
This document covers the authorization mechanisms used in the API, outlining how permissions are managed and enforced.

### Role-Based Access Control
- The system defines multiple user roles: admin, customer, merchant, as seen in the `Users` model in `models.py`.
- The `role` column in the `Users` model specifies the user's role.

### Securing Endpoints
- Some endpoints are restricted based on user roles, particularly in `admin.py`.
- The `check_admin_user_auth` function in `admin.py` is used to verify if the user has admin privileges.

### Example Code
```python
def check_admin_user_auth(user):
    if user is None or user.get('user_role').lower() != 'admin':
        raise HTTPException(status_code=401, detail='Authentication Failed')
```

### Endpoints
* **GET /admin/transactions**: Accessible only by users with admin role.
* **GET /admin/users**: Accessible only by users with admin role.


### Error Handling
* Unauthorized access attempts result in 'HTTPException' with status code '401 Unauthorized'.