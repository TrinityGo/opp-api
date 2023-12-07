"""this module contains the admin API routes"""
# Standard imports
from typing import Annotated
# Third-party imports
from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from sqlalchemy.orm import Session
from backend.routers.auth import get_current_user
# Local imports
from backend.models.models import Users, Transactions
from backend.db.database import SessionLocal
# Create the router
router = APIRouter(prefix='/admin', tags=['admin'])


def get_db():
    """Get the database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# when an API uses this, it will enforce authorization
DbDependency = Annotated[Session, Depends(get_db)]

# when an API uses this, it will enforce authorization
UserDependency = Annotated[dict, (Depends(get_current_user))]

# when an API uses this, it will enforce authorization
user_dependency = Annotated[dict, (Depends(get_current_user))]


@router.get("/transactions",status_code=status.HTTP_200_OK,tags=["Administrative Control"])
async def read_all_transactions(user: UserDependency, db: DbDependency):
    """This function returns all transactions in the database. 
    It is only accessible to admin users."""
    check_admin_user_auth(user)
    return db.query(Transactions).all()


@router.get("/users",status_code=status.HTTP_200_OK, tags=["Administrative Control"])
async def read_all_users(user: UserDependency, db: DbDependency):
    """This function returns all users in the database. It is only accessible to admin users."""
    check_admin_user_auth(user)
    return db.query(Users).all()

# when an API uses this, it will enforce authorization
def check_admin_user_auth(user):
    """This function checks if the user is an admin user. If not, it raises an exception."""
    if user is None or user.get('user_role').lower() != 'admin':
        raise HTTPException(status_code=401, detail='Authentication Failed')
