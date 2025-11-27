from fastapi import FastAPI

from app.db import init_db
from app.routers import customers, transaction, invoice, time, plans, customer_plan

app = FastAPI(
    lifespan=init_db(),
    responses={404: {"description": "Not found"}},
)

# Routes
app.include_router(customers.router, prefix="/api")
app.include_router(plans.router, prefix="/api")
app.include_router(customer_plan.router, prefix="/api")
app.include_router(transaction.router, prefix="/api")
app.include_router(invoice.router, prefix="/api")
app.include_router(time.router, prefix="/api")
