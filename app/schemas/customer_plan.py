from pydantic import BaseModel

from app.models.customer_plan import StatusEnum


class CustomerPlanBase(BaseModel):
    plan_id: int
    customer_id: int
    status: StatusEnum


class CustomerPlanCreate(CustomerPlanBase):
    pass


class CustomerPlanUpdate(BaseModel):
    plan_id: int | None = None
    customer_id: int | None = None


class CustomerPlanRead(CustomerPlanBase):
    id: int
