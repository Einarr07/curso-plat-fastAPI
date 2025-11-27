from pydantic import BaseModel


class PlanBase(BaseModel):
    name: str
    price: int
    description: str | None = None


class PlanCreate(PlanBase):
    pass


class PlanUpdate(BaseModel):
    name: str
    price: int
    description: str | None = None


class PlanRead(PlanBase):
    id: int
