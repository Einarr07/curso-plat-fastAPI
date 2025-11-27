from pydantic import BaseModel


class CustomerPlanBase(BaseModel):
    plan_id: int
    customer_id: int


class CustomerPlanCreate(CustomerPlanBase):
    pass


class CustomerPlanUpdate(BaseModel):
    plan_id: int | None = None
    customer_id: int | None = None


class CustomerPlanRead(CustomerPlanBase):
    id: int
