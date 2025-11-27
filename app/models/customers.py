from typing import List, TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .invoice import Invoice


class Customer(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    description: str | None = None
    email: str
    age: int

    invoices: List['Invoice'] = Relationship(back_populates="customer")
