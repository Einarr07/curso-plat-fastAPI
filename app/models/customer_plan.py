from enum import Enum

from sqlmodel import SQLModel, Field


class StatusEnum(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class CustomerPlan(SQLModel, table=True):
    __tablename__ = "customers_plans"
    id: int | None = Field(primary_key=True)
    plan_id: int = Field(foreign_key="plans.id")
    customer_id: int = Field(foreign_key="customers.id")
    status: StatusEnum = Field(default=StatusEnum.ACTIVE)
