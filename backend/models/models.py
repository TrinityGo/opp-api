"""This file contains the models for the database"""
# Standard imports
from datetime import datetime
# Third-party imports
from sqlalchemy import Column, Integer, String
from sqlalchemy import Boolean, ForeignKey, Float, DateTime, JSON
# Local imports
from backend.db.database import Base


class Users(Base):
    """This class represents the Users table in the database."""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True, unique=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    first_name = Column(String)
    surname = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String)  # customer/merchant/admin
    phone_number = Column(String)


class Transactions(Base):
    """This class represents the Transactions table in the database.
    """
    __tablename__ = 'transactions'

    transaction_id = Column(Integer, primary_key=True, index=True, unique=True)
    customer_id = Column(Integer, ForeignKey("users.id"))
    merchant_id = Column(Integer)  # foreignkey("merchants.id")
    customer_bank_info = Column(String)
    merchant_bank_info = Column(String)
    encrypted_card_number = Column(JSON)  # encrypted_card_number
    amount = Column(Float)
    time_stamp = Column(DateTime, default=datetime.utcnow)
    status = Column(String)
    payment_type = Column(String)  # credit_card/debit_card