"""
Module for authentication-related routes and functions.

This module defines routes and functions related to user authentication using
FastAPI.

Functions:
    - create_user: Create a new user in the database.
    - login_for_access_token: Log in a user and generate an access token.
    - authenticate_user: Authenticate a user based on provided credentials.
    - create_access_token: Create an access token for a user.
    - get_current_user:
        Retrieve information about the current user from the provided token.

Classes:
    - CreateUserRequest: Pydantic model for creating a new user.
    - Token: Pydantic model for representing an access token.

Routes:
    - POST /auth/: Create a new user.
    - POST /auth/token/: Log in and retrieve an access token.
    - POST /auth/user/: Retrieve information about the current user.

Dependencies:
    - get_db: Dependency function to get a database session.

Variables:
    - router: FastAPI APIRouter for handling authentication routes.
    - SECRET_KEY: Secret key for JWT token creation.
    - ALGORITHM: Algorithm used for JWT token encoding.
    - bcrypt_context: Passlib CryptContext for password hashing.
    - oauth2_bearer:
        OAuth2PasswordBearer instance for handling token authentication.
    - DbDependency: Dependency for getting a database session.

Note:
    This module requires the presence of environment variables for SECRET_KEY
    and ALGORITHM.
"""
# Standard imports
import os
from datetime import timedelta, datetime
# Third-party imports
from typing import Annotated, Any
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from pydantic import BaseModel
from starlette import status
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from dotenv import load_dotenv
from passlib.context import CryptContext
# Local imports
from backend.models.models import Users
from backend.db.database import SessionLocal

# Create the router
router = APIRouter(prefix='/auth', tags=['auth'])

# Load environment variables
load_dotenv()  # take environment variables from .env.

# These are used to create the signature for a JWT
SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")

# This is used to hash the password
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

# Dependency function to get a database session
def get_db():
    """This function gets a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# when an API uses this, it will enforce authorization
DbDependency = Annotated[Session, Depends(get_db)]

# Pydantic model for creating a new user
class CreateUserRequest(BaseModel):
    """This class represents the request body for creating a new user."""
    email: str
    username: str
    first_name: str
    surname: str
    password: str
    role: str

# Pydantic model for representing an access token
class Token(BaseModel):
    """This class represents an access token."""
    access_token: str
    token_type: str

# Route for creating a new user
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: DbDependency,
                      create_user_request: CreateUserRequest):
    """This function creates a new user in the database. It is only"""
    try:
        create_user_model = Users(
            email=create_user_request.email,
            username=create_user_request.username,
            first_name=create_user_request.first_name,
            surname=create_user_request.surname,
            role=create_user_request.role,
            hashed_password=bcrypt_context.hash(create_user_request.password),
            is_active=True
        )

        db.add(create_user_model)
        db.commit()
        return {"message": "User created successfully"}

    except Exception as e:
        message = str(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Failed to Create User. Error Info: '
                            + message) from e


@router.post("/token/", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: DbDependency
):
    """This function logs in a user and generates an access token."""
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user')

    # Create token from the authenticated user
    token = create_access_token(user.username, user.id,
                                user.role, timedelta(minutes=30))

    return {'access_token': token, 'token_type': 'bearer'}


def authenticate_user(username: str, password: str, db: DbDependency) -> Any:
    """This function authenticates a user based on provided credentials."""
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False

    return user


def create_access_token(username: str, user_id: int,
                        role: str, expires_delta: timedelta):
    """This function creates an access token for a user."""
    claims = {'sub': username, 'id': user_id, 'role': role}
    expires = datetime.utcnow() + expires_delta
    claims.update({'exp': expires})
    token = jwt.encode(claims, SECRET_KEY, algorithm=ALGORITHM)
    return token


@router.post("/user", status_code=status.HTTP_201_CREATED)
async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    """This function retrieves information about the current user from the provided token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        user_role: str = payload.get('role')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not validate user')
        return {'username': username, 'id': user_id, 'user_role': user_role}
    except JWTError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user') from exc
