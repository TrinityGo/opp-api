# Authentication Documentation
- **Title:** Authentication Documentation
- **Course:** NEU CS5500 Fall 2023
- **Date:** Dec 7, 2023
- **Author:** Yiwen Wang, Xinyi Gao, Yijia Ma
- **Version:** 2.0
- **Contents:** Explain how to obtain and use API keys or token

**Revision History**
|Date|Version|Description|Author|
|:----:|:----:|:----:|:----:|
|Nov 9, 2023|1.0|Initial release| Yiwen Wang|
|Dec 7, 2023|2.0|Update API| Yiwen Wang|

## Overview
This document describes the authentication process for the API. The authentication is handled primarily in `auth.py`, where users are authenticated via JWT tokens.

### Authentication Flow
- The authentication is performed via the `/auth/token/` endpoint.
- The process involves verifying user credentials and returning a JWT token for successful authentication.

### Endpoints
#### POST /auth/token/
- **Description**: Authenticate the user and receive an access token.
- **Request**:
  ```json
  {
    "username": "user@example.com",
    "password": "password123"
  }
  ```
- **Response**
```json
{
  "access_token": "jwt_token_here",
  "token_type": "bearer"
}
```
- **Security Details**
- Passwords are hashed using bcrypt, as implemented in 'auth.py'.
- JWTs are used for maintaining the authentication state, with 'SECRET_KEY' and 'ALGORITHM' stored in environment variables.
- The 'bcrypt_context' object in 'auth.py' manages password hashing and verification.

- **Example Code**
```python
@router.post("/token/", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Dbdependency):
        # Authenticate the user
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user')

    # Create token from the authenticated user
    token = create_access_token(user.username, user.id, user.role, timedelta(minutes=30))

    return {'access_token': token, 'token_type': 'bearer'}
```

- **Environment Variables**
- 'SECRET_KEY' and 'ALGORITHM' are used in token creation and are loaded from '.env' files.

- **Error Handling**
- 'HTTPException' with status code '401 Unauthorized' is raised if authentication fails.


