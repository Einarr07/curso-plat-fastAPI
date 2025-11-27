from typing import List, Optional, TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .customers import Customer
    from .transaction import Transaction


class Invoice(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    customer_id: int = Field(foreign_key="customer.id")
    total: int = 0

    customer: 'Customer' = Relationship(back_populates="invoices")
    transactions: List['Transaction'] = Relationship(back_populates="invoice")

    @property
    def amount_total(self) -> int:
        return sum(t.amount for t in self.transactions)
