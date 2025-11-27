# app/schemas/transaction.py
from typing import Optional

from sqlmodel import SQLModel

from app.schemas import CustomerRead


class TransactionBase(SQLModel):
    amount: int
    description: str


class TransactionCreate(TransactionBase):
    customer_id: int
    invoice_id: int | None = None


class TransactionUpdate(SQLModel):
    amount: Optional[int] = None
    description: Optional[str] = None
    customer_id: Optional[int] = None
    invoice_id: Optional[int] = None


class TransactionRead(TransactionBase):
    id: int
    customer_id: int
    customer: CustomerRead | None = None
    invoice_id: int | None = None
