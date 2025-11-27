from typing import List, TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship

from .customer_plan import CustomerPlan

if TYPE_CHECKING:
    from .invoice import Invoice
    from .transaction import Transaction
    from .plan import Plan


class Customer(SQLModel, table=True):
    __tablename__ = "customers"
    id: int | None = Field(default=None, primary_key=True)
    name: str
    description: str | None = None
    email: str
    age: int

    transactions: List['Transaction'] = Relationship(back_populates="customer")

    invoices: List['Invoice'] = Relationship(back_populates="customer")

    plans: List['Plan'] = Relationship(back_populates="customers", link_model=CustomerPlan)
