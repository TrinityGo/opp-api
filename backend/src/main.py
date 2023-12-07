from fastapi import FastAPI

from src.models import models
from backend.src.db.database import engine
from backend.src.routers import auth, admin, transactions

# application
app = FastAPI()

# sets up database defined in engine
models.Base.metadata.create_all(bind=engine)

# Set API endpoints on router
app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(transactions.router)
