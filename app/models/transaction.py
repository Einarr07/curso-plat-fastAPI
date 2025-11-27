from sqlmodel import SQLModel, Field, Relationship

from .invoice import Invoice


class Transaction(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    amount: int
    description: str
    invoice_id: int = Field(foreign_key="invoice.id")
    invoice: "Invoice" = Relationship(back_populates="transactions")
