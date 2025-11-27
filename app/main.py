from fastapi import FastAPI

from app.db import create_all_tables
from app.routers import customers, transaction, time

app = FastAPI(
    lifespan=create_all_tables,
    responses={404: {"description": "Not found"}},
)

# Routes
app.include_router(customers.router, prefix="/api")
app.include_router(transaction.router, prefix="/api")
app.include_router(time.router, prefix="/api")
