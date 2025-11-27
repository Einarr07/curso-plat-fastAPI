# app/schemas/invoice.py
from typing import List, Optional

from sqlmodel import SQLModel, Field

from app.schemas.customers import CustomerRead
from app.schemas.transaction import TransactionRead


class InvoiceBase(SQLModel):
    customer_id: int


class InvoiceCreate(InvoiceBase):
    total: int = 0


class InvoiceUpdate(SQLModel):
    customer_id: Optional[int] = None
    total: Optional[int] = None


class InvoiceRead(InvoiceBase):
    id: int
    total: int

    customer: Optional[CustomerRead] = None
    transactions: List[TransactionRead] = Field(default_factory=list)

    @property
    def amount_total(self) -> int:
        return sum(t.amount for t in self.transactions)
