from typing import Optional

from sqlmodel import SQLModel, Field


class TransactionBase(SQLModel):
    amount: int
    description: str


class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(SQLModel):
    amount: Optional[int] = None
    description: Optional[str] = None


class TransactionRead(TransactionBase):
    id: int | None = Field(default=None, primary_key=True)
