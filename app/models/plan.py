from typing import TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship

from .customer_plan import CustomerPlan

if TYPE_CHECKING:
    from .customers import Customer


class Plan(SQLModel, table=True):
    __tablename__ = "plans"
    id: int | None = Field(default=None, primary_key=True)
    name: str
    price: int
    description: str

    customers: list['Customer'] = Relationship(back_populates="plans", link_model=CustomerPlan)
