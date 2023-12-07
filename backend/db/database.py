"""This file is used to create the database connection and session."""
# Standard imports
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# eclarative_base() function is deprecated and has been moved in SQLAlchemy 2.0
from sqlalchemy.orm import declarative_base
# from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = 'sqlite:///./payment_software.db'
# SQLALCHEMY_DATABASE_URL = 'postgresql://cs5500:12345@localhost/TodoApplicationDatabase'

# Create the database engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for the models
Base = declarative_base()
