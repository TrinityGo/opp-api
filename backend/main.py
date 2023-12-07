"""
Main FastAPI application.

This module sets up the FastAPI application, initializes the database,
and includes routers for authentication, admin, and transactions.
"""
from fastapi import FastAPI

from backend.models import models
from backend.db.database import engine
from backend.routers import auth, admin, transactions

# application
app = FastAPI()

# sets up database defined in engine
models.Base.metadata.create_all(bind=engine)

# Set API endpoints on router
app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(transactions.router)
