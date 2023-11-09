from db.database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Float, DateTime
from datetime import datetime


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    first_name = Column(String)
    surname = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String)
    phone_number = Column(String)

# TODO Transactions?
class Transactions(Base):
    __tablename__ = 'transactions'
    
    transaction_id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("users.id")) # TODO Users.id?
    merchant_id = Column(Integer) # foreignkey("merchants.id")
    encrypted_info = Column(String)
    amount = Column(Float)
    time_stamp = Column(DateTime, default=datetime.utcnow)
    status = Column(String)
    
    







