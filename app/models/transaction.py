from typing import TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .customers import Customer
    from .invoice import Invoice


class Transaction(SQLModel, table=True):
    __tablename__ = "transactions"
    id: int | None = Field(default=None, primary_key=True)
    amount: int
    description: str

    customer_id: int = Field(default=None, foreign_key='customers.id')
    customer: 'Customer' = Relationship(back_populates='transactions')

    invoice_id: int = Field(foreign_key="invoices.id")
    invoice: 'Invoice' = Relationship(back_populates="transactions")
